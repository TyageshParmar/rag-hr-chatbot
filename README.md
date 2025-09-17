# RAG HR Policy Chatbot

A Retrieval-Augmented Generation (RAG) chatbot that answers questions about HR policies using document embeddings and large language models. This project leverages LangChain, FAISS, Groq LLM API, and Ollama embeddings to build an intelligent, context-aware chatbot.

---

## Features

- Extracts and processes text from HR policy PDF documents
- Splits documents into manageable chunks and generates embeddings
- Uses FAISS for fast similarity search
- Applies BM25 re-ranking for more relevant source retrieval
- Integrates with Groq LLM API for natural language answers
- Caches queries for faster repeated responses
- Simple Streamlit frontend for interactive Q&A
- Fully containerizable for easy deployment

---

## Project Structure

```

.
├── api.py                  # FastAPI backend exposing /query endpoint
├── chatbot\_streamlit.py    # Streamlit UI for chatting with the bot
├── pipeline.py             # Core RAG pipeline: ingestion, indexing, querying
├── requirements.txt        # Python dependencies
├── test\_ollama\_embed.py    # Test script for Ollama embeddings
├── HR-Policy.pdf           # Sample HR policy document (input)
├── .env                    # Environment variables (excluded from repo)
├── Dockerfile              # Containerization setup (if added)
└── README.md               # This file

````

---

## Setup & Installation

### 1. Clone the repository

```bash
git clone https://github.com/TyageshParmar/rag-hr-chatbot.git
cd rag-hr-chatbot
````

### 2. Create a Python environment and install dependencies

```bash
python -m venv venv
source venv/bin/activate     # Linux/macOS
venv\Scripts\activate        # Windows

pip install -r requirements.txt
```

### 3. Configure environment variables

Create a `.env` file in the project root with the following:

```env
GROQ_API_KEY=your_groq_api_key_here
OLLAMA_URL=http://localhost:11434
```

**Important:** Do not commit `.env` or any secrets to the repository.

### 4. Run the backend API server

```bash
uvicorn api:app --reload
```

### 5. Run the Streamlit frontend

```bash
streamlit run chatbot_streamlit.py
```

---

## Usage

* Open your browser at the URL shown by Streamlit (typically [http://localhost:8501](http://localhost:8501)).
* Enter your backend API URL (default is `http://127.0.0.1:8000/docs`).
* Ask questions about the HR policy document.
* View answers with cited page numbers and source snippets.

---

## Development

* Modify `pipeline.py` to customize document ingestion, chunking, embedding, or querying.
* Change LLM or embedding models in `pipeline.py` as needed.
* Extend the frontend UI in `chatbot_streamlit.py`.

---

## Security Notes

* **Do not expose your API keys or secrets publicly.**
* Use `.gitignore` to exclude `.env` files.
* GitHub secret scanning may block pushes with exposed secrets.

---

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

## Acknowledgements

* [LangChain](https://github.com/langchain-ai/langchain)
* [Ollama Embeddings](https://github.com/nomic-ai/ollama)
* [Groq LLM API](https://www.groq.com/)
* [FAISS](https://github.com/facebookresearch/faiss)
* [Streamlit](https://streamlit.io/)

---
Let me know if you want me to help generate `.gitignore` or Dockerfile next!
```
