# rin/agent.py
from rin.llm import query_ollama
from rin.memory import retrieve_memories
from rin.memory_update import update_memory


class RinAgent:
    def __init__(self, memory_path="data/memories.json"):
        self.memory_path = memory_path

    def generate_caption(self, topic: str):
        """
        Generates a caption using Rin's memories + the given topic,
        and updates her memory.
        """
        # 1. Retrieve top relevant memories
        memories = retrieve_memories(topic, self.memory_path)
        context = "\n".join([f"- {m}" for m in memories])

        # 2. Build prompt for Ollama
        prompt = f"""
You are Rin, an AI influencer living in Shanghai.
You are playful, wholesome, and luxurious.
Use the following memories to stay consistent with your personality:
{context}

Write a short Instagram caption (2-3 sentences max)
about this topic: "{topic}"

You may reference past posts naturally.
Keep it authentic, Gen Z tone, and add 2-3 fitting hashtags.
        """

        # 3. Generate caption using Ollama
        caption = query_ollama(prompt)

        # 4. Update memory with the new caption
        update_memory(
            caption,
            self.memory_path,
            metadata={"type": "caption", "topic": topic, "persona": "rin"}
        )

        # 5. Return the final caption
        return caption.strip()
