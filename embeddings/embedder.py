from langchain.embeddings import HuggingFaceInstructEmbeddings

def get_embeddings():
    return HuggingFaceInstructEmbeddings(
        model_name="hkunlp/instructor-small",
        model_kwargs={"device": "cpu"}  # or "cuda" if GPU available
    )
