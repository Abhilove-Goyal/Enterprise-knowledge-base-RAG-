from langchain_text_splitters import RecursiveCharacterTextSplitter
from config.settings import settings
def split_documents(documents):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=settings.CHUNK_SIZE,
        chunk_overlap=settings.CHUNK_OVERLAP
    )
    return splitter.split_documents(documents)
