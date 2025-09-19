# test_ollama_embed.py
from langchain_ollama import OllamaEmbeddings

emb = OllamaEmbeddings(model="nomic-embed-text", base_url="http://localhost:11434")

try:
    vecs = emb.embed_documents(["HR policy leave rules", "Maternity benefits"])
    print("Embedding success ✅")
    print("Number of vectors:", len(vecs))
    print("Dimensions:", len(vecs[0]))
except Exception as e:
    print("Embedding failed ❌")
    print(e)