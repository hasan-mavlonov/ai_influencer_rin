# rin/llm.py
import subprocess
import sys
import base64
import io
import torch
from diffusers import StableDiffusionPipeline


def query_ollama(prompt, model="llama3"):
    """
    Query a local Ollama model and return its text response.
    Compatible with Windows UTF-8 output.
    """
    try:
        command = ["ollama", "run", model]
        process = subprocess.Popen(
            command,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            encoding="utf-8",
            errors="ignore"
        )

        stdout, stderr = process.communicate(input=prompt)

        if stderr.strip():
            print("⚠️ Ollama stderr:", stderr.strip())

        if not stdout.strip():
            return "No response received."

        response_lines = [line.strip() for line in stdout.splitlines() if line.strip()]
        return "\n".join(response_lines)

    except Exception as e:
        return f"[Error querying Ollama: {e}]"


# ---------------------------------------------------------
# 🧠 Load the Stable Diffusion model (v2.1)
# ---------------------------------------------------------
# Much better realism, especially for faces and lighting.
# Works locally if you have ~6–8 GB VRAM.
# If not, we can add CPU offload later.

print("🔄 Loading Stable Diffusion 2.1 model...")

sd_model = StableDiffusionPipeline.from_pretrained(
    "stabilityai/stable-diffusion-2-1",
    torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32
)

if torch.cuda.is_available():
    sd_model = sd_model.to("cuda")
else:
    print("⚠️ CUDA not available — using CPU (will be slower).")

print("✅ Model loaded successfully.")


def generate_image(prompt: str):
    """
    Generate an image using Stable Diffusion locally.
    Returns raw PNG bytes.
    """
    print(f"🎨 Generating image for prompt: {prompt}")
    image = sd_model(prompt).images[0]

    buf = io.BytesIO()
    image.save(buf, format="PNG")
    return buf.getvalue()
