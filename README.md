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

#### 1. **Docker Usage Instructions**

Add a section like this:

````md
## 🚀 Run with Docker

You can pull and run the chatbot using Docker without setting up Python or dependencies locally.

### 1. Pull the image

```bash
docker pull tyageshparmar/rag-hr-chatbot:latest
````

### 2. Run the container

```bash
docker run -p 8000:8000 -p 8501:8501 tyageshparmar/rag-hr-chatbot:latest
```

Then open:

* 🔗 [http://localhost:8501](http://localhost:8501) – Streamlit frontend
* 🔗 [http://localhost:8000/docs](http://localhost:8000/docs) – FastAPI Swagger UI

````

---

#### 2. **Screenshots**
Include at least:
- 📄 A snapshot of the Streamlit chat UI
- 📑 Optional: API `/docs` view
This helps recruiters and visitors quickly understand the value of your project.

---

#### 3. **Live Demo (Optional)**
If you deploy this somewhere (e.g., Render, Hugging Face Spaces, Railway), add:

```md
## 🌐 Live Demo

Try the chatbot here: [your-link-here]
````

---

#### 4. **Security Notes (Complete the section)**

Your section ends mid-sentence. Suggest finishing it like this:

```md
## 🔐 Security Notes

- Do not commit `.env` files or API keys to version control.
- Use secrets management when deploying to cloud platforms.
- Add rate-limiting and CORS policies in production setups.
```
