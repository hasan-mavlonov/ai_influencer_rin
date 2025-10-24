import json
from pathlib import Path
from uuid import uuid4
from .utils import get_embedding  # your embedding helper


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

    # Create new memory entry
    new_entry = {
        "id": str(uuid4()),  # unique ID
        "content": new_text,
        "metadata": metadata
    }

    # Append
    memories.append(new_entry)

    # Save
    with open(memory_path, "w", encoding="utf-8") as f:
        json.dump(memories, f, ensure_ascii=False, indent=2)

    print(f"🧠 Added new memory ({len(memories)} total).")
