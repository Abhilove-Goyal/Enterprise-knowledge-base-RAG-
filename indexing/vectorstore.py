from langchain_community.vectorstores import FAISS
import os

def build_index(chunks, embeddings, index_path):
    os.makedirs(index_path, exist_ok=True)
    vectorstore = FAISS.from_documents(chunks, embeddings)
    vectorstore.save_local(index_path)

def load_index(embeddings, index_path):
    return FAISS.load_local(
        index_path,
        embeddings,
        allow_dangerous_deserialization=True
    )
