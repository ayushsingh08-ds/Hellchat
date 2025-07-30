from utils.extract_text import extract_text
from utils.embed_store import embed_and_store, query_vector_store

def process_and_store(file_path, file_name):
    text = extract_text(file_path)
    embed_and_store(text, file_name)

# Exporting query function
__all__ = ['process_and_store', 'query_vector_store']
