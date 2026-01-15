from InstructorEmbedding import INSTRUCTOR
from langchain.embeddings.base import Embeddings

class InstructorEmbeddings(Embeddings):
    def __init__(self, model_name: str = "hkunlp/instructor-small"):
        self.model = INSTRUCTOR(model_name)

    def embed_documents(self, texts: list[str]) -> list[list[float]]:
        pairs = [["Represent the semantic embedding:", t] for t in texts]
        return self.model.encode(pairs)

def get_embeddings():
    return InstructorEmbeddings("hkunlp/instructor-small")
