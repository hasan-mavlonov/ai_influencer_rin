# rin/memory.py
import json
from sentence_transformers import SentenceTransformer, util
import torch

model = SentenceTransformer('all-MiniLM-L6-v2')


def load_memories(memory_path):
    with open(memory_path, "r", encoding="utf-8") as f:
        return json.load(f)


def retrieve_memories(query, memory_path, top_k=3):
    """
    Retrieve the top K relevant memories based on semantic similarity.
    Works with structured memories (id, content, metadata).
    """
    memories = load_memories(memory_path)
    if not memories:
        return []

    memory_texts = [m["content"] for m in memories]

    memory_embeddings = model.encode(memory_texts, convert_to_tensor=True)
    query_embedding = model.encode(query, convert_to_tensor=True)

    scores = util.pytorch_cos_sim(query_embedding, memory_embeddings)[0]
    top_results = torch.topk(scores, k=min(top_k, len(memories)))

    return [memory_texts[idx] for idx in top_results.indices]
