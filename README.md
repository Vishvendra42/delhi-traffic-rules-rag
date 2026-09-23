# Delhi Traffic Rules Assistant

An AI-powered Retrieval-Augmented Generation (RAG) chatbot for Delhi
traffic rules, penalties, driving licences, vehicle documents, road
safety, speed limits and related procedures.

## 1. Overview

This project uses Retrieval-Augmented Generation instead of asking an
LLM to answer entirely from its pretrained knowledge.

The flow is:

``` text
User Question
      ↓
Question Embedding
      ↓
FAISS Similarity Search
      ↓
Relevant Delhi Traffic Rule Chunks
      ↓
Groq LLM
      ↓
Final Answer
```

The project uses a Delhi-specific master knowledge base and combines
semantic retrieval with LLM-based answer generation.

## 2. Technologies

  Technology              Purpose
  ----------------------- ---------------------------
  Python                  Main programming language
  Sentence Transformers   Generate text embeddings
  all-MiniLM-L6-v2        Embedding model
  FAISS                   Vector similarity search
  LangChain               LLM integration
  Groq                    LLM inference
  openai/gpt-oss-20b      Current LLM
  FastAPI                 Backend REST API
  Streamlit               Frontend

## 3. Project Structure

``` text
traffic_rules_assistant-main/
│
├── api/
│   └── app.py
│
├── data/
│   └── delhi/
│       ├── raw/
│       │   └── MASTER_DELHI_TRAFFIC_KNOWLEDGE_BASE.txt
│       │
│       └── processed/
│           ├── audit_rules.json
│           ├── delhi_chunks.json
│           └── delhi_faiss_index.idx
│
├── frontend/
│   └── streamlit_app.py
│
├── src/
│   ├── __init__.py
│   ├── chunking.py
│   ├── embedding.py
│   ├── retriever.py
│   ├── generator.py
│   ├── text_extraction.py
│   ├── master_corpus.py
│   └── main.py
│
├── .env
├── .gitignore
├── README.md
├── requirements.txt
├── pyproject.toml
└── .python-version
```

## 4. Knowledge Base

The main source is:

``` text
data/delhi/raw/MASTER_DELHI_TRAFFIC_KNOWLEDGE_BASE.txt
```

It contains Delhi traffic information covering areas such as driving
licences, registration, insurance, PUCC, penalties, challans, road
safety, signs, speed limits, parking, commercial vehicles, emergency
vehicles, citizen services and FAQs.

`audit_rules.json` is kept as a supporting audit artifact. It is not
required by the runtime retrieval path.

## 5. RAG Pipeline

### Step 1: Chunking

`src/chunking.py` reads the master knowledge base and creates
overlapping text chunks.

Current configuration:

``` text
Chunk size: 2000 characters
Overlap: 300 characters
```

The current knowledge base produces approximately 95 chunks.

Output:

``` text
data/delhi/processed/delhi_chunks.json
```

### Step 2: Embeddings

`src/embedding.py` uses:

``` text
all-MiniLM-L6-v2
```

to convert each chunk into a numerical vector.

The model produces 384-dimensional embeddings.

Output:

``` text
data/delhi/processed/delhi_faiss_index.idx
```

### Step 3: Retrieval

`src/retriever.py` converts the user's question into an embedding and
searches the FAISS index.

``` text
Question
   ↓
Embedding
   ↓
FAISS
   ↓
Top-K Relevant Chunks
```

The retriever finds information; it does not generate the final answer.

### Step 4: Generation

`src/generator.py` combines the retrieved chunks with the user's
question and sends them to Groq through LangChain.

The current model is:

``` text
openai/gpt-oss-20b
```

with temperature:

``` text
0.3
```

## 6. Backend

`api/app.py` exposes the RAG system through FastAPI.

Main endpoint:

``` text
POST /ask
```

Example request:

``` json
{
  "query": "What is the fine for driving without a licence?",
  "top_k": 5
}
```

Example response:

``` json
{
  "question": "What is the fine for driving without a licence?",
  "answer": "..."
}
```

Health endpoint:

``` text
GET /
```

FastAPI documentation:

``` text
http://localhost:8000/docs
```

## 7. Frontend

`frontend/streamlit_app.py` provides the chatbot interface.

The frontend communicates with FastAPI rather than directly accessing
FAISS or Groq.

``` text
Streamlit
    ↓
FastAPI
    ↓
Generator
    ↓
Retriever
    ↓
FAISS
    ↓
Groq
```

## 8. Installation

Create and activate a virtual environment:

``` powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

Install dependencies:

``` powershell
pip install -r requirements.txt
```

## 9. API Key

The application requires a Groq API key.

Set it in PowerShell for the current terminal:

``` powershell
$env:GROQ_API_KEY="YOUR_GROQ_API_KEY"
```

Never commit the real API key to GitHub.

Recommended `.gitignore` entries:

``` text
.venv/
.env
__pycache__/
*.pyc
```

If the application is configured to load `.env` automatically, the root
`.env` can contain:

``` text
GROQ_API_KEY=YOUR_GROQ_API_KEY
```

## 10. Run the Application

The application uses two terminals.

### Terminal 1: FastAPI

From the project root:

``` powershell
uvicorn api.app:app --reload
```

Backend:

``` text
http://localhost:8000
```

### Terminal 2: Streamlit

From the project root:

``` powershell
streamlit run frontend/streamlit_app.py
```

Frontend:

``` text
http://localhost:8501
```

## 11. Testing

Test the generator:

``` powershell
python -m src.generator
```

Test retrieval:

``` powershell
python test_retriever.py
```

Example questions:

``` text
What is the fine for driving without a licence?

What is the penalty for not wearing a helmet?

What is the penalty for driving without insurance?

Can a learner licence holder drive alone?

What is the fine for triple riding?

What documents should I carry while driving in Delhi?
```

## 12. Rebuilding the RAG Data

If the master knowledge base is changed, rebuild the processed data in
this order:

``` powershell
python src/text_extraction.py
python src/chunking.py
python src/embedding.py
```

The resulting files are:

``` text
data/delhi/processed/delhi_chunks.json
data/delhi/processed/delhi_faiss_index.idx
```

Do not run these steps every time the chatbot is started. They are
data-preparation steps.

## 13. Understanding the Four Main RAG Files

### chunking.py

Splits the knowledge base into smaller overlapping chunks.

### embedding.py

Converts chunks into numerical embeddings and creates the FAISS index.

### retriever.py

Finds the chunks that are most similar to the user's question.

### generator.py

Passes the retrieved information and question to the LLM and returns the
answer.

A simple interview explanation is:

> First, I split the Delhi traffic knowledge base into chunks. I convert
> those chunks into embeddings using Sentence Transformers and store
> them in FAISS. When a user asks a question, I embed the question and
> retrieve the most relevant chunks. These chunks are provided as
> context to the Groq LLM, which generates the final answer.

## 14. Retrieval vs Generation

These are two separate stages.

### Retrieval

``` text
Question
   ↓
Embedding
   ↓
FAISS
   ↓
Relevant Chunks
```

### Generation

``` text
Question + Relevant Chunks
          ↓
       Groq LLM
          ↓
       Answer
```

If retrieval returns irrelevant information, generation can also suffer.
Therefore both stages should be evaluated separately.

## 15. Current Configuration

  Component             Configuration
  --------------------- -------------------------------------------
  Knowledge base        Delhi Traffic Rules Master Knowledge Base
  Chunk size            2000 characters
  Overlap               300 characters
  Current chunks        Approximately 95
  Embedding model       all-MiniLM-L6-v2
  Embedding dimension   384
  Vector database       FAISS
  Retrieval             Top-K similarity search
  LLM                   openai/gpt-oss-20b
  Temperature           0.3
  Backend               FastAPI
  Frontend              Streamlit

## 16. Limitations

The quality of the chatbot depends on the quality and freshness of its
knowledge base and retrieval results.

Important limitations include:

-   Character-based chunks can sometimes contain multiple unrelated
    pieces of information.
-   Retrieval can occasionally return broad or partially relevant
    chunks.
-   Traffic rules, penalties and administrative procedures can change.
-   Dynamic traffic advisories require updated source data.
-   An LLM can misunderstand retrieved information.
-   Important legal or time-sensitive matters should be checked against
    current official sources.

## 17. Possible Future Improvements

-   Section-aware or semantic chunking
-   Metadata-based retrieval
-   Hybrid keyword and vector search
-   Reranking retrieved chunks
-   Source citations in the UI
-   Automated RAG evaluation
-   Periodic knowledge-base updates
-   Better retrieval diagnostics
-   Multi-turn conversation support
-   Production deployment

## 18. Disclaimer

This project is intended for educational and informational purposes.

Traffic rules, penalties, notifications, procedures, fees and
administrative requirements may change. Important or time-sensitive
matters should be verified against the relevant current official
authorities.

## 19. Quick Start

After installation and API-key setup:

**Terminal 1**

``` powershell
uvicorn api.app:app --reload
```

**Terminal 2**

``` powershell
streamlit run frontend/streamlit_app.py
```

Then open:

``` text
http://localhost:8501
```

Ask a Delhi traffic question and the system will retrieve relevant
knowledge and generate an answer.

------------------------------------------------------------------------

## Project Summary

``` text
Knowledge Base
      ↓
Chunking
      ↓
Embeddings
      ↓
FAISS
      ↓
Retriever
      ↓
Groq LLM
      ↓
FastAPI
      ↓
Streamlit
```

**Delhi Traffic Rules Assistant --- Python + Sentence Transformers +
FAISS + LangChain + Groq + FastAPI + Streamlit**
