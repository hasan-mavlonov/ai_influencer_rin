from .memory_update import retrieve_relevant_memories, update_memory
from .utils import ollama_generate
import random
import json

class RinAgent:
    def __init__(self, memory_path="data/memories.json"):
        self.memory_path = memory_path

    def generate_topic(self):
        """
        Generate Rin's next post topic.
        Mostly new topics, occasionally connected to past topics.
        """
        # Load past topics
        try:
            with open(self.memory_path, "r", encoding="utf-8") as f:
                memories = json.load(f)
            past_topics = [m["metadata"].get("topic") for m in memories if m["metadata"].get("type") == "caption"]
        except FileNotFoundError:
            past_topics = []

        # Decide whether to make a connected topic or new topic
        connect_to_past = random.random() < 0.3  # 30% chance to connect to past

        if connect_to_past and past_topics:
            # Pick a past topic to subtly connect
            past_topic = random.choice(past_topics)
            prompt = f"""
            You are Rin — a stylish influencer living in Shanghai.
            Based on your past posts, suggest a new Instagram photo topic idea
            that is subtly connected to this past topic: "{past_topic}".
            Keep it specific, fresh, and interesting.
            Respond with just the topic phrase.
            """
        else:
            # Completely new topic
            prompt = f"""
            You are Rin — a stylish influencer living in Shanghai.
            Based on your previous posts, suggest a new Instagram photo topic idea.
            Avoid repeating the exact same topics: {past_topics}.
            Keep it specific and interesting (like “late-night ramen with neon lights” or “Sunday art museum stroll”).
            Respond with just the topic phrase.
            """

        topic = ollama_generate(prompt)
        return topic.strip().replace('"', "")

    def generate_caption(self, topic=None):
        """
        Generates a caption either for a provided topic, or chooses one automatically.
        """
        if not topic:
            topic = self.generate_topic()
            print(f"🎯 Rin chose her next topic: {topic}")

        # 🧠 Recall past memories
        relevant = retrieve_relevant_memories(topic, self.memory_path)
        context = "\n".join([f"- {m['content']}" for m in relevant])

        prompt = f"""
You are Rin — a playful, wholesome, luxurious influencer living in Shanghai.
Your tone is warm, stylish, and natural.
Use these past memories to keep your personality consistent:

{context}

Now write a short Instagram caption (2–3 sentences)
about the topic: "{topic}"
Make it sound authentic, Gen-Z aesthetic, and add fitting emojis & hashtags.
"""

        caption = ollama_generate(prompt)

        # 🧩 Save new caption as memory
        metadata = {"type": "caption", "topic": topic, "persona": "rin"}
        update_memory(caption, self.memory_path, metadata)

        return caption
