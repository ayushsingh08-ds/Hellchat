<h2 align="center">KneadQuality AI</h2>

**QWalT (Quality & Workflow AI Tool)** is your intelligent AI-powered assistant designed to:

- Answer Quality Assurance (QA)-related queries
- Analyze Standard Operating Procedures (SOPs)
- Suggest actionable improvements in process and workflow
- Help enterprises optimize operations through conversational AI

## Tech Stack

- **Frontend**: React.js, CSS
- **Routing**: React Router DOM
- **Backend**: Python with FastAPI
- **AI & Search**: FAISS, Transformers, RAG (Retrieval-Augmented Generation)
- **Model**: OpenRouter LLM API
- **Hosting**: Render, Vercel

## How It Works

1. **User uploads a document or asks a QA-related query**
2. **FAISS** finds the most relevant chunks from stored SOPs
3. A **prompt** is built combining user query and matched content
4. **LLM** generates a high-quality, contextual answer
5. The result is returned to the user in a clean UI

## Setup Instructions

### 1. Clone the repo

```bash
git clone https://github.com/your-username/QWalT.git
cd QWalT
```

### 2. Create .env file with

OPENROUTER_API_KEY=your_api_key_here

### 3. Backend Setup

```bash
cd backend
pip install -r requirements.txt
uvicorn app:app --reload
```

### 4. Frontend Setup

```bash
cd ../frontend
npm install
npm run dev
```

## Developers:

<a href="https://github.com/ayushsingh08-ds">@Ayush Singh</a><br>
<a href="https://github.com/ArjiJethin">@Arji Jethin Naga Sai Eswar</a><br> 
<a href="https://github.com/alurubalakarthikeya">@Aluru Bala Karthikeya</a>
