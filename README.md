# Document Processor with LLM Integration

A document processing system that combines document loading, embeddings, vector search, and LLM-powered query responses.

## Project Overview

This project processes various document formats (PDF, DOCX) and enables semantic search using embeddings and FAISS vector store. It integrates with LLM services to provide intelligent responses based on document content.

## Project Structure

```
projectno1/
├── api/                    # FastAPI application
│   └── main.py            # API endpoints
├── database/              # Database layer
│   ├── connection.py      # Database connection setup
│   ├── crud.py            # CRUD operations
│   ├── models.py          # SQLAlchemy models
│   └── schemas.py         # Pydantic schemas
├── graph/                 # Workflow orchestration
│   ├── nodes.py           # Workflow nodes
│   ├── state.py           # Workflow state management
│   └── workflow.py        # Workflow definition
├── parsers/               # Response parsing
│   └── responseparser.py   # LLM response parser
├── frontend/              # Frontend application
│   └── app.py             # Frontend interface
├── faiss_index/           # Vector store
│   └── index.faiss        # FAISS index file
├── documentProcessor.py   # Document processing logic
├── llmservice.py          # LLM service integration
├── logic.py               # Core business logic
└── prompt_Builder.py      # Prompt construction
```

## Setup

### Prerequisites
- Python 3.8+
- Virtual environment (venv)

### Installation

1. Create and activate virtual environment:
```bash
python -m venv venv
.\venv\Scripts\Activate.ps1  # Windows
# or
source venv/bin/activate     # Linux/Mac
```

2. Install dependencies:
```bash
pip install langchain langchain-community langchain-text-splitters
pip install sqlalchemy
pip install fastapi uvicorn
pip install sentence-transformers faiss-cpu
pip install python-docx pypdf
```

## Usage

### Document Processing
```python
from documentProcessor import *

# Load and process documents
docs = load_documents("path/to/documents")
splits = split_documents(docs)
vectorstore = create_vectorstore(splits)
```

### Running the API
```bash
python -m uvicorn api.main.py --reload
```

### Running the Frontend
```bash
streamlit run frontend/app.py
```

## Features

- **Multi-format Document Loading**: Support for PDF and DOCX files
- **Semantic Search**: Vector-based similarity search using FAISS
- **LLM Integration**: Query answering using language models
- **Query History**: Track and store all queries and responses
- **REST API**: FastAPI-based endpoints for document processing
- **Vector Store**: Persistent FAISS index for fast retrieval

## Database Models

### QueryHistory
- `id`: Primary key
- `filename`: Source document filename
- `question`: User query
- `response`: LLM response
- `created_at`: Timestamp when record created
- `updated_at`: Timestamp when record updated

## Contributing

1. Create a feature branch
2. Make your changes
3. Test thoroughly
4. Submit a pull request



### Demo
[Watch Demo](./demo_GRB1w81i.mp4)


