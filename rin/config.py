# rin/config.py
import os

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")
MEMORY_PATH = os.path.join(DATA_DIR, "memories.json")
VECTORSTORE_PATH = os.path.join(DATA_DIR, "vectorstore.json")
POSTS_PATH = os.path.join(DATA_DIR, "posts.json")
POSTS_IMAGE_DIR = os.path.join(DATA_DIR, "rin_posts")

RIN_PERSONA_PROMPT = """
You are Rin — a stylish, warm, slightly poetic influencer living in Shanghai.
You write short captions, full of feeling and aesthetics.
"""
