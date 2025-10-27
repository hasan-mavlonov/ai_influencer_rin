# rin/actions.py
import os, json, uuid, datetime
from .config import POSTS_PATH, POSTS_IMAGE_DIR
from .utils import save_json, load_json
from .llm import generate_image  # function we'll define soon


def create_post_entry(topic, caption, image_path):
    posts = load_json(POSTS_PATH)
    new_post = {
        "id": str(uuid.uuid4()),
        "topic": topic,
        "caption": caption,
        "image_path": image_path,
        "timestamp": datetime.datetime.now().isoformat()
    }
    posts.append(new_post)
    save_json(posts, POSTS_PATH)
    return new_post


def generate_image_for_topic(topic):
    prompt = f"A stylish young woman named Rin in Shanghai, {topic}, cinematic lighting, Instagram aesthetic."
    image_bytes = generate_image(prompt)
    os.makedirs(POSTS_IMAGE_DIR, exist_ok=True)
    image_path = os.path.join(POSTS_IMAGE_DIR, f"{uuid.uuid4()}.png")
    with open(image_path, "wb") as f:
        f.write(image_bytes)
    return image_path
