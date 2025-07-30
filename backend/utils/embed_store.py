"""
Ultra-lightweight embedding store using simple keyword matching
Memory footprint: ~10-20MB total
No external ML dependencies required
"""
import os
import pickle
import re
import textwrap
import math
from collections import Counter, defaultdict

VECTOR_DIR = "vector_db"
if not os.path.exists(VECTOR_DIR):
    os.makedirs(VECTOR_DIR)

class SimpleVectorizer:
    """Lightweight TF-IDF implementation without sklearn"""
    
    def __init__(self, max_features=500):
        self.max_features = max_features
        self.vocabulary = {}
        self.idf_values = {}
        
    def _tokenize(self, text):
        """Simple tokenization"""
        # Convert to lowercase and extract words
        text = text.lower()
        words = re.findall(r'\b[a-zA-Z]{2,}\b', text)
        
        # Remove common stop words
        stop_words = {
            'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 
            'of', 'with', 'by', 'is', 'are', 'was', 'were', 'be', 'been', 'have', 
            'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could', 'should',
            'this', 'that', 'these', 'those', 'i', 'you', 'he', 'she', 'it', 'we', 'they'
        }
        
        return [word for word in words if word not in stop_words and len(word) > 2]
    
    def fit_transform(self, documents):
        """Fit vectorizer and transform documents"""
        # Tokenize all documents
        tokenized_docs = [self._tokenize(doc) for doc in documents]
        
        # Build vocabulary from most frequent words
        word_freq = Counter()
        for tokens in tokenized_docs:
            word_freq.update(set(tokens))  # Count document frequency, not term frequency
        
        # Select top words by document frequency
        most_common = word_freq.most_common(self.max_features)
        self.vocabulary = {word: idx for idx, (word, _) in enumerate(most_common)}
        
        # Calculate IDF values
        num_docs = len(documents)
        for word in self.vocabulary:
            doc_count = sum(1 for tokens in tokenized_docs if word in tokens)
            self.idf_values[word] = math.log(num_docs / (doc_count + 1))
        
        # Create TF-IDF vectors
        vectors = []
        for tokens in tokenized_docs:
            vector = [0.0] * len(self.vocabulary)
            token_counts = Counter(tokens)
            total_tokens = len(tokens)
            
            for word, count in token_counts.items():
                if word in self.vocabulary:
                    tf = count / total_tokens
                    idf = self.idf_values[word]
                    vector[self.vocabulary[word]] = tf * idf
            
            vectors.append(vector)
        
        return vectors
    
    def transform(self, documents):
        """Transform new documents using fitted vocabulary"""
        if not self.vocabulary:
            return []
            
        vectors = []
        for doc in documents:
            tokens = self._tokenize(doc)
            vector = [0.0] * len(self.vocabulary)
            token_counts = Counter(tokens)
            total_tokens = len(tokens) if tokens else 1
            
            for word, count in token_counts.items():
                if word in self.vocabulary:
                    tf = count / total_tokens
                    idf = self.idf_values.get(word, 0)
                    vector[self.vocabulary[word]] = tf * idf
            
            vectors.append(vector)
        
        return vectors

def cosine_similarity_simple(vec1, vec2):
    """Simple cosine similarity implementation"""
    if not vec1 or not vec2:
        return 0.0
        
    dot_product = sum(a * b for a, b in zip(vec1, vec2))
    magnitude1 = math.sqrt(sum(a * a for a in vec1))
    magnitude2 = math.sqrt(sum(a * a for a in vec2))
    
    if magnitude1 == 0 or magnitude2 == 0:
        return 0.0
    
    return dot_product / (magnitude1 * magnitude2)

def embed_and_store(text, file_name):
    """Lightweight document embedding using simple TF-IDF"""
    # Same chunking strategy as before
    section_pattern = r"(?:\n|^)(\d[\d\.]*[\)\.]?|Step \d+|Section \d+)[^\n]*\n"
    sections = re.split(section_pattern, text)

    structured_chunks = []
    i = 0
    while i < len(sections):
        if i < len(sections) and re.match(section_pattern, sections[i] if i < len(sections) else ""):
            heading = sections[i].strip()
            if i + 1 < len(sections):
                content = sections[i + 1].strip()
                full_text = f"{heading}: {content}"
                chunks = textwrap.wrap(full_text, width=450, break_long_words=False, break_on_hyphens=False)
                structured_chunks.extend(chunks)
                i += 2
            else:
                i += 1
        else:
            if i < len(sections):
                plain = sections[i].strip()
                if plain:
                    chunks = textwrap.wrap(plain, width=450, break_long_words=False, break_on_hyphens=False)
                    structured_chunks.extend(chunks)
            i += 1

    # Filter out empty chunks
    structured_chunks = [chunk for chunk in structured_chunks if chunk.strip()]
    
    if not structured_chunks:
        print(f"Warning: No chunks extracted from {file_name}")
        return

    # Create simple TF-IDF vectors
    vectorizer = SimpleVectorizer(max_features=300)  # Reduced feature count
    try:
        vectors = vectorizer.fit_transform(structured_chunks)
    except Exception as e:
        print(f"Error creating vectors: {e}")
        return

    # Save vectors and vectorizer
    vectors_path = os.path.join(VECTOR_DIR, f"{file_name}_vectors.pkl")
    vectorizer_path = os.path.join(VECTOR_DIR, f"{file_name}_vectorizer.pkl")
    chunks_path = os.path.join(VECTOR_DIR, f"{file_name}_chunks.pkl")

    with open(vectors_path, "wb") as f:
        pickle.dump(vectors, f)
    
    with open(vectorizer_path, "wb") as f:
        pickle.dump(vectorizer, f)

    with open(chunks_path, "wb") as f:
        pickle.dump(structured_chunks, f)

    print(f"Stored {len(structured_chunks)} chunks for {file_name}")

def query_vector_store(query, file_name, top_k=3):
    """Lightweight vector search using simple cosine similarity"""
    vectors_path = os.path.join(VECTOR_DIR, f"{file_name}_vectors.pkl")
    vectorizer_path = os.path.join(VECTOR_DIR, f"{file_name}_vectorizer.pkl")
    chunks_path = os.path.join(VECTOR_DIR, f"{file_name}_chunks.pkl")

    # Check if files exist
    if not all(os.path.exists(path) for path in [vectors_path, vectorizer_path, chunks_path]):
        return "Document not indexed."

    try:
        # Load saved data
        with open(vectors_path, "rb") as f:
            doc_vectors = pickle.load(f)
        
        with open(vectorizer_path, "rb") as f:
            vectorizer = pickle.load(f)
        
        with open(chunks_path, "rb") as f:
            chunks = pickle.load(f)

        # Transform query using the same vectorizer
        query_vectors = vectorizer.transform([query])
        
        if not query_vectors or not query_vectors[0]:
            return "No relevant information found."
        
        query_vector = query_vectors[0]
        
        # Calculate similarities with all document vectors
        similarities = []
        for doc_vector in doc_vectors:
            similarity = cosine_similarity_simple(query_vector, doc_vector)
            similarities.append(similarity)
        
        # Get top-k most similar chunks
        indexed_similarities = list(enumerate(similarities))
        indexed_similarities.sort(key=lambda x: x[1], reverse=True)
        
        # Filter out very low similarity scores and get top results
        results = []
        for idx, similarity in indexed_similarities[:top_k]:
            if similarity > 0.05:  # Minimum similarity threshold
                results.append(chunks[idx])
        
        if not results:
            return "No relevant information found in the document."
            
        return "\n\n".join(results)

    except Exception as e:
        print(f"Error in query_vector_store: {e}")
        return "Error retrieving information from document."
