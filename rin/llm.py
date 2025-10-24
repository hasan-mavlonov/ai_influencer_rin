# rin/llm.py
import subprocess
import sys


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
            encoding="utf-8",  # ✅ Force UTF-8 output
            errors="ignore"  # ✅ Ignore stray invalid bytes
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
