# # api.py
# from fastapi import FastAPI
# from pydantic import BaseModel
# from pipeline import RAGPipeline
# import os

# app = FastAPI()
# PIPELINE = None

# class QueryRequest(BaseModel):
#     query: str


# # @app.post("/query")
# # def query_bot(req: QueryRequest):
# #     global PIPELINE
# #     if PIPELINE is None:
# #         pdf_path = os.getenv("HR_PDF_PATH", "HR-Policy.pdf")
# #         PIPELINE = RAGPipeline(pdf_path=pdf_path, persist_dir="./faiss_index")
# #     return PIPELINE.query(req.query)

# @app.post("/query")
# def query_bot(req: QueryRequest):
#     global PIPELINE
#     if PIPELINE is None:
#         pdf_path = os.getenv("HR_PDF_PATH", "HR-Policy.pdf")
#         PIPELINE = RAGPipeline(pdf_path=pdf_path, persist_dir="./faiss_index")
#     try:
#         result = PIPELINE.query(req.query)
#         return result
#     except Exception as e:
#         import traceback
#         traceback.print_exc()
#         return {"error": str(e)}



# api.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from pipeline import RAGPipeline
import os

app = FastAPI(title="HR Policy Chatbot API")

# Config
pdf_path = "HR-Policy.pdf"   # Path to your HR policy PDF
ollama_url = "http://localhost:11434"
PIPELINE = None


class QueryRequest(BaseModel):
    query: str


@app.on_event("startup")
def startup_event():
    global PIPELINE
    try:
        if not os.path.exists(pdf_path):
            raise FileNotFoundError(f"PDF file not found: {pdf_path}")

        PIPELINE = RAGPipeline(
            pdf_path=pdf_path,
            persist_dir="./faiss_index",#ollama_url=ollama_url
        )
        print("✅ Pipeline initialized successfully")
    except Exception as e:
        print(f"❌ Failed to initialize pipeline: {e}")
        PIPELINE = None


@app.post("/query")
def query_endpoint(request: QueryRequest):
    if PIPELINE is None:
        return {
            "answer": "⚠️ Backend pipeline is not ready. Please check logs.",
            "sources": []
        }

    try:
        result = PIPELINE.query(request.query)
        return result
    except Exception as e:
        return {
            "answer": f"⚠️ An error occurred while processing your query: {str(e)}",
            "sources": []
        }
