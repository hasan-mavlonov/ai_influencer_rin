# rin/utils.py
from sentence_transformers import SentenceTransformer

# Load model once
embedding_model = SentenceTransformer('all-MiniLM-L6-v2')


def get_embedding(text: str):
    """
    Returns a list of floats (embedding vector) for a given text.
    """
    return embedding_model.encode(text).tolist()
