from dotenv import load_dotenv
load_dotenv()  # make sure env vars are loaded first

from config.settings import settings
from ingestion.loaders import load_pdfs
from ingestion.cleaner import clean_documents
from chunking.splitter import split_documents
from embeddings.embedder import get_embeddings
from indexing.vectorstore import build_index
from fastapi import FastAPI

# create FastAPI instance
from api.app import app  # import your existing FastAPI instance

# optional: run indexing on startup
@app.on_event("startup")
def startup_indexing():
    print("Starting indexing...")
    docs = load_pdfs(settings.DATA_PATH)
    docs = clean_documents(docs)
    chunks = split_documents(docs)
    embeddings = get_embeddings()
    build_index(chunks, embeddings, settings.INDEX_PATH)
    print("Indexing done!")
