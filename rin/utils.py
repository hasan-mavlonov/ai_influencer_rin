import os
import json
from sentence_transformers import SentenceTransformer

# Load sentence transformer for embeddings
embedding_model = SentenceTransformer("all-MiniLM-L6-v2")


def get_embedding(text: str):
    """Returns a list of floats (embedding vector) for a given text."""
    return embedding_model.encode(text).tolist()


def ollama_generate(prompt: str, model: str = "llama3"):
    """Generate text from Ollama."""
    import subprocess
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


# ✅ NEW: JSON helpers for universal use
def load_json(path, default=None):
    """Safely load JSON or return default."""
    if not os.path.exists(path):
        return default if default is not None else []
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError:
        print(f"⚠️ Corrupted JSON file: {path}, resetting.")
        return default if default is not None else []


def save_json(data, path):
    """Save JSON safely with UTF-8 and indentation."""
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
