# pipeline.py
import os
from typing import List, Dict
from langchain_community.document_loaders import PyPDFLoader, UnstructuredPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_ollama import OllamaEmbeddings, OllamaLLM
from rank_bm25 import BM25Okapi
from langchain_groq import ChatGroq
from dotenv import load_dotenv
import os

# Simple in-memory cache
CACHE: Dict[str, Dict] = {}


class RAGPipeline:
    def __init__(self, pdf_path: str, persist_dir: str = "./faiss_index", ollama_url: str = "http://localhost:11434"):
        self.pdf_path = pdf_path
        self.persist_dir = persist_dir
        self.ollama_url = ollama_url

        # ✅ Use dedicated embedding model
        self.embeddings = OllamaEmbeddings(
            model="nomic-embed-text",
            base_url=self.ollama_url
        )

        # # ✅ Use chat model for answers
        # self.llm = OllamaLLM(
        #     model="gemma2:2b",
        #     base_url=self.ollama_url)
        
        # Load .env file
        load_dotenv()

        # Use Groq LLM
        # self.llm = ChatGroq(
        #     api_key=os.getenv("GROQ_API_KEY"),
        #     model_name="mixtral-8x7b-32768"  # You can also try: llama3-70b-8192
        # )

        self.llm = ChatGroq(
            api_key=os.getenv("GROQ_API_KEY"),
            model="llama-3.1-8b-instant", # <-- use this (or llama-3.3-70b-versatile)
            temperature=0
        )

        # Load and split PDF
        docs = self._load_pdf(pdf_path)
        splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
        self.chunks = splitter.split_documents(docs)

        # Build or load FAISS index
        if os.path.exists(self.persist_dir):
            # self.vectorstore = FAISS.load_local(self.persist_dir, self.embeddings)
            self.vectorstore = FAISS.load_local(
                self.persist_dir,
                self.embeddings,
                allow_dangerous_deserialization=True)

        else:
            print("⚡ Building FAISS index for the first time... this may take a while.")
            self.vectorstore = FAISS.from_documents(self.chunks, self.embeddings)
            os.makedirs(self.persist_dir, exist_ok=True)
            self.vectorstore.save_local(self.persist_dir)
        print("✅ FAISS index ready")

    def _clean_text(self, text: str) -> str:
        """Remove excessive line breaks and extra spaces for clean output."""
        text = text.replace("\n", " ")   # remove line breaks
        text = " ".join(text.split())    # normalize spaces
        return text

    def _load_pdf(self, filepath):
        _, ext = os.path.splitext(filepath)
        if ext.lower() == ".pdf":
            try:
                loader = PyPDFLoader(filepath)
                docs = loader.load()
            except Exception:
                loader = UnstructuredPDFLoader(filepath)
                docs = loader.load()
        else:
            with open(filepath, "r", encoding="utf-8") as f:
                t = f.read()
            docs = [{"page_content": t, "metadata": {"page": 0}}]

        # ✅ Clean text + ensure metadata consistency
        for i, d in enumerate(docs):
            d.page_content = self._clean_text(d.page_content)
            if "page" not in d.metadata:
                d.metadata["page"] = d.metadata.get("page", i + 1)
        return docs

    def rerank_bm25(self, query: str, docs: List):
        corpus = [d.page_content for d in docs]
        tokenized = [c.split() for c in corpus]
        bm25 = BM25Okapi(tokenized)
        scores = bm25.get_scores(query.split())
        ranked = sorted(zip(docs, scores), key=lambda x: x[1], reverse=True)
        return [doc for doc, _ in ranked]

    def query(self, query: str, top_k: int = 10, rerank_k: int = 5):
        key = query.strip().lower()
        if key in CACHE:
            return CACHE[key]

        # Retrieve candidates
        candidates = self.vectorstore.similarity_search(query, k=top_k)

        # Re-rank with BM25
        reranked = self.rerank_bm25(query, candidates)[:rerank_k]

        # Build context
        context_parts = []
        for d in reranked:
            page = d.metadata.get("page", "Unknown")
            snippet = self._clean_text(d.page_content)
            context_parts.append(f"[Page {page}] {snippet}")

        context = "\n\n---\n\n".join(context_parts)

        # Prompt
        prompt = (
            "Use the context below to answer the question concisely. "
            "Cite page numbers when relevant.\n\n"
            f"Context:\n{context}\n\nQuestion: {query}\n\nAnswer:"
        )

        # Query LLM
        response = self.llm.invoke(prompt)
        answer = response.content  # <- get only the text part


        sources = [
            {
                "page": d.metadata.get("page", "Unknown"),
                "snippet": self._clean_text(d.page_content)[:300]
            }
            for d in reranked
        ]

        result = {"answer": answer, "sources": sources}
        CACHE[key] = result
        return result