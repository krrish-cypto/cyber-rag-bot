# 🛡️ Cyber Threat Intelligence RAG Bot

A sophisticated offline-capable Retrieval Augmented Generation (RAG) bot designed for cybersecurity threat intelligence and incident response. This bot leverages local language models and vector databases to provide context-aware security insights without requiring internet connectivity.

## ✨ Features

- **Offline-First Architecture**: Operates completely offline using local embeddings and vector database
- **RAG-Powered Responses**: Retrieves relevant security documents before generating answers
- **NIST Protocol Support**: Specialized knowledge for cybersecurity incident response and NIST frameworks
- **Dual Interface**: 
  - Streamlit UI for interactive chat
  - FastAPI REST API for programmatic access
- **Local Document Ingestion**: Processes PDF files from your local `/data` folder
- **Telemetry Disabled**: Privacy-first design with all telemetry and tracking disabled
- **Zero External Dependencies**: No reliance on cloud APIs or external services

## 📋 Prerequisites

- Python 3.8+
- pip (Python package manager)

## 🚀 Installation

### 1. Clone or extract the project
```bash
cd cyber-rag-bot-main
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Prepare your knowledge base
Create a `data` folder in the project root and add your cybersecurity PDF documents:
```
cyber-rag-bot-main/
├── data/
│   ├── nist_framework.pdf
│   ├── incident_response_guide.pdf
│   └── security_protocols.pdf
├── app.py
├── api.py
└── ...
```

### 4. Build the vector database
Run the ingestion script to process documents and create the ChromaDB vector store:
```bash
python ingest.py
```

Output:
```
Loading security documents...
Chunking text...
Initializing local embedding model...
Saving vectors to ChromaDB...
Success! Database saved to ./chroma_db
```

## 📁 Project Structure

```
cyber-rag-bot-main/
├── app.py              # Streamlit UI application
├── api.py              # FastAPI REST API
├── rag_engine.py       # Core RAG logic and LLM integration
├── ingest.py           # Document ingestion and vector DB creation
├── requirements.txt    # Python dependencies
├── data/               # Your security PDF documents (create this)
└── chroma_db/          # Vector database storage (auto-generated)
```

## 💻 Usage

### Option 1: Streamlit Web UI (Recommended)
```bash
streamlit run app.py
```
- Opens in your browser at `http://localhost:8501`
- Interactive chat interface with animations
- Real-time threat intelligence responses

### Option 2: FastAPI REST API
```bash
uvicorn api:app --reload
```
- API available at `http://localhost:8000`
- API documentation at `http://localhost:8000/docs`

**Example API Request:**
```bash
curl -X POST "http://localhost:8000/chat" \
  -H "Content-Type: application/json" \
  -d '{"query": "What are the NIST incident response steps?"}'
```

**Response:**
```json
{
  "answer": "Based on NIST guidelines, the incident response steps are...",
  "sources": ["document_name.pdf"]
}
```

## 🔧 Core Components

### `ingest.py`
Processes PDF documents from the `/data` folder and creates a ChromaDB vector database:
- Loads documents using PyPDFDirectoryLoader
- Chunks text with overlap for context preservation
- Creates embeddings using HuggingFace's all-MiniLM-L6-v2 model
- Stores vectors in ChromaDB for fast retrieval

### `rag_engine.py`
Main RAG engine that handles queries:
- Loads the ChromaDB vector database
- Retrieves relevant documents
- Handles greeting detection
- Generates context-aware responses
- Offline environment variables enabled

### `app.py`
Streamlit interface with:
- Cybersecurity-themed UI with animations
- Chat message display
- Real-time interaction
- Custom CSS styling

### `api.py`
FastAPI REST API with:
- `/chat` POST endpoint for querying
- JSON request/response format
- Automatic API documentation

## 🌐 Offline Capabilities

This project is designed to work **completely offline** with the following configurations:

```python
os.environ["HF_HUB_OFFLINE"] = "1"              # Disable HuggingFace Hub access
os.environ["HF_HUB_DISABLE_TELEMETRY"] = "1"   # No telemetry
os.environ["ANONYMIZED_TELEMETRY"] = "False"   # Disable anonymous tracking
```

**First run**: Requires internet to download the embedding model (`all-MiniLM-L6-v2`)  
**Subsequent runs**: Fully offline operation

## 📦 Dependencies

| Package | Purpose |
|---------|---------|
| `fastapi` | REST API framework |
| `uvicorn` | ASGI server for FastAPI |
| `streamlit` | Web UI framework |
| `langchain` | LLM orchestration |
| `langchain-community` | Vector store & embeddings |
| `langchain-huggingface` | HuggingFace integration |
| `chromadb` | Vector database |
| `sentence-transformers` | Embedding model support |
| `pypdf` | PDF processing |
| `python-dotenv` | Environment variable management |

## 🔐 Security Considerations

- All data processing happens locally
- No external API calls (unless explicitly configured with LangChain-Groq)
- Models and vectors stored locally in `/chroma_db`
- Environment telemetry disabled by default
- No internet requirement after initial setup

## 🐛 Troubleshooting

**Issue**: "No documents found!" error
- **Solution**: Ensure PDFs are in the `/data` folder, then run `python ingest.py` again

**Issue**: Module not found errors
- **Solution**: Reinstall requirements: `pip install -r requirements.txt`

**Issue**: Slow first response
- **Solution**: First run downloads the embedding model (~80MB). Subsequent runs are faster

**Issue**: Port already in use
- **Solution**: For Streamlit: `streamlit run app.py --server.port 8502`
- **Solution**: For API: `uvicorn api:app --port 8001`

## 📚 Example Knowledge Base

This bot works best with:
- NIST Cybersecurity Framework documentation
- Incident Response playbooks
- Security audit guidelines
- Threat intelligence reports
- Compliance frameworks (ISO 27001, CIS Controls, etc.)

## 🚦 Getting Started Guide

1. **Setup**: `pip install -r requirements.txt`
2. **Add Documents**: Place security PDFs in `/data` folder
3. **Index Documents**: `python ingest.py`
4. **Run Interface**: `streamlit run app.py`
5. **Ask Questions**: Use the chat interface to query your knowledge base

##  Author

**Krishna Dubey**

## 📝 License

MIT License

Copyright (c) 2026 Krishna Dubey

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

## 🤝 Contributing

Contributions are welcome! Feel free to:
- Add more sophisticated NLP models
- Improve document chunking strategies
- Enhance the UI
- Add support for more document formats

---

**Built for cybersecurity professionals who need offline threat intelligence** 🛡️
