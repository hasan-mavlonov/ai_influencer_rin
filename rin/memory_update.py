# rin/memory_update.py
import json
from pathlib import Path
from uuid import uuid4
from .utils import get_embedding  # your embedding helper
import json
import numpy as np
from .utils import get_embedding


def cosine_similarity(a, b):
    a, b = np.array(a), np.array(b)
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))


def retrieve_relevant_memories(topic, memory_path, top_n=3):
    topic_emb = get_embedding(topic)
    with open(memory_path, "r", encoding="utf-8") as f:
        memories = json.load(f)

    scored = []
    for m in memories:
        if "embedding" in m:
            score = cosine_similarity(topic_emb, m["embedding"])
            scored.append((score, m))
    scored.sort(reverse=True, key=lambda x: x[0])
    return [m for _, m in scored[:top_n]]


def update_memory(new_text: str, memory_path: str, metadata=None):
    """
    Append a new memory (post or trait) while keeping the structured format.
    """
    path = Path(memory_path)
    path.parent.mkdir(parents=True, exist_ok=True)

    # Load existing memories
    if path.exists():
        with open(path, "r", encoding="utf-8") as f:
            memories = json.load(f)
    else:
        memories = []

    # Default metadata
    if metadata is None:
        metadata = {"type": "caption", "persona": "rin"}

    embedding = get_embedding(new_text)

    new_entry = {
        "id": str(uuid4()),
        "content": new_text,
        "metadata": metadata
    }

    # Append
    memories.append(new_entry)

    # Save
    with open(memory_path, "w", encoding="utf-8") as f:
        json.dump(memories, f, ensure_ascii=False, indent=2)

    print(f"🧠 Added new memory ({len(memories)} total).")
