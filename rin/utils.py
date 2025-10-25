# rin/utils.py
import subprocess
import json
from sentence_transformers import SentenceTransformer

# Load sentence transformer for embeddings
embedding_model = SentenceTransformer("all-MiniLM-L6-v2")


def get_embedding(text: str):
    """
    Returns a list of floats (embedding vector) for a given text.
    """
    return embedding_model.encode(text).tolist()


def ollama_generate(prompt: str, model: str = "llama3"):

    try:
        result = subprocess.run(
            ["ollama", "run", model],
            input=prompt.encode("utf-8"),
            capture_output=True,
            check=True,
        )
        return result.stdout.decode("utf-8").strip()
    except subprocess.CalledProcessError as e:
        print("⚠️ Ollama generation error:", e.stderr.decode("utf-8"))
        return "(Error generating text)"
