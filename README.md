# AskMyDocs
A RAG-based AI Assistant for Travel Insurance Documents

## Overview

AskMyDocs is an intelligent document assistant that lets users upload their travel insurance docuemnts and ask natural language questions about their coverage. By combining advanced PDF processing with RAG technology, it delivers accurate answers grounded in the actual policy text.

## Features

* PDF Document Processing: Extract and process text from complex insurance.
* Advanced RAG Pipeline: Retrieve relevant document sections before generating answers.
* Multiple LLM Support: Compatible with DeepSeek and OpenAI models
* Vector Search: FAISS powered semantic search for accurate information retrieval.
* Context-Aware Responses: Answers include citations to relevant policy sections.
* Easy API Integration: Well-documented FastAPI endpoints for seamless integration.
* Clean, Modern UI: Intuitive Next.js frontend for document management and chat.

### Tech Stack

* Backend: Python 3.9+, FastAPI.
* LLM: DeepSeek API.
* RAG Tools: LangChain, FAISS.
* Document Processing: PyMuPDF.
* Frontend: Next.js.

### Installation

Prerequisites:
* Python 3.9+
* DeepSeek API Key

Setup
1. Clone the repository:
```bash
  git clone https://github.com/tylerbeckb/AskMyDocs.git
  cd AskMyDocs
```

2. Create and activate a virtual environment:
```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
    pip install -r requirements.txt
```

4. Set up environment variables:
```bash
    cp .env.example .env
    # Edit .env to add your API key
```

## Usage

Starting the Server
```bash
    python -m src.app
    # Or: uvicorn src.app:app --reload
```

The API will be available at http://localhost:8000. Visit http://localhost:8000/docs for the interactive API documentation.

#### Basic Workflow

###### 1. Upload a document:
```bash
    curl -X POST "http://localhost:8000/api/upload" \
        -H "accept: application/json" \
        -H "Content-Type: multipart/form-data" \
        -F "file=@travel_insurance_policy.pdf"
```

###### 2. Ask a question:
```bash
    curl -X POST "http://localhost:8000/api/query" \
        -H "accept: application/json" \
        -H "Content-Type: application/json" \
        -d '{"query": "What does my policy cover for lost baggage?", "top_k": 3}'
```

## API Documentation

Endpoints

POST /api/upload

Upload a PDF document for indexing

Request:

* file: PDF file (multipart/form-data)

Response:
```bash
    {
        "filename": "travel_policy.pdf",
        "chunks": 0,
        "status": "processing"
    }
```
POST /api/query

Query the indexed documents

Request:
```bash
    {
        "query": "What's covered for emergency medical expenses?",
        "top_k": 3
    }
```

Response:
```bash
    {
        "answer": "Your policy covers emergency medical expenses up to $1,000,000 including...",
        "sources": [
            {
                "source": "travel_policy.pdf",
                "section": "MEDICAL COVERAGE"
            }
        ]
    }
```

## Project Structure
```bash
    askmydocs/
        ├── src/
        │   ├── api/
        │   │   ├── exceptions.py    # Custom exception classes
        │   │   ├── routes.py        # FastAPI route definitions
        │   │   └── schemas.py       # Pydantic data models
        │   ├── data/
        │   │   ├── loader.py        # Document loading utilities
        │   │   └── processor.py     # Document chunking and processing
        │   ├── models/
        │   │   ├── embeddings.py    # Embedding model configurations
        │   │   └── llm.py           # LLM service implementation
        │   ├── rag/
        │   │   ├── generator.py     # Answer generation logic
        │   │   ├── indexing.py      # Document indexing pipeline
        │   │   └── retriever.py     # Context retrieval system
        │   ├── utils/
        │   │   ├── pdf_parser.py    # PDF text extraction
        │   │   └── vector_store.py  # Vector database interface
        │   └── app.py               # Main application entry point
        ├── tests/                    # Test modules
        ├── data/                     # Data storage directory
        ├── .env.example              # Environment variables template
        ├── requirements.txt          # Project dependencies
        └── README.md                 
```

## Testing

Run the test suite with:
```bash
    pytest
```

## Acknowledgments

* LangChain for providing the RAG framework
* DeepSeek AI for the language model capabilities
* FastAPI team for the excellent web framework