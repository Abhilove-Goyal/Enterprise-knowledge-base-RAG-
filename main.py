from dotenv import load_dotenv
from config.settings import settings
from ingestion.loaders import load_pdfs
from ingestion.cleaner import clean_documents
from chunking.splitter import split_documents
from embeddings.embedder import get_embeddings
from indexing.vectorstore import build_index
from fastapi import FastAPI

# create FastAPI instance
app = FastAPI()

# import your existing routers or API logic
from api.app import router  # adjust if you have routers
app.include_router(router)
load_dotenv()

def run_indexing():
    docs = load_pdfs("data/docs")
    docs = clean_documents(docs)
    chunks = split_documents(docs)
    embeddings = get_embeddings()
    index_path = settings.INDEX_PATH
    build_index(chunks, embeddings, index_path)

if __name__ == "__main__":
    run_indexing()
