import asyncio
import traceback
import re
import os
from datetime import datetime

import ollama

# ================= CONFIG =================

MODEL_NAME = "Your Model Here"

SYSTEM_PROMPT = """
Your Custom Prompt Here
"""


# ================= LOGGER =================

def log(section, message):
    timestamp = datetime.now().strftime("%H:%M:%S")
    print(f"\n[{timestamp}] [{section}]")
    print(message)
    print("-" * 60)


# ================= OUTPUT POLISHER =================

def polish_output(text: str):

    if not text:
        return "No response generated."

    text = text.strip()

    while "\n\n\n" in text:
        text = text.replace("\n\n\n", "\n\n")

    return text


# ================= OLLAMA REQUEST =================

def ask_local_llm(prompt=None, image_path=None):

    messages = [
        {
            "role": "system",
            "content": SYSTEM_PROMPT
        },
        {
            "role": "user",
            "content": prompt if prompt else "Analyze this image."
        }
    ]

    if image_path:
        messages[1]["images"] = [image_path]
        log("IMAGE INPUT", image_path)

    log("LLM REQUEST", f"Prompt: {prompt}")

    response = ollama.chat(
        model=MODEL_NAME,
        messages=messages
    )

    output = response["message"]["content"]

    log("LLM RESPONSE", output)

    return output


# ================= ASYNC WRAPPER =================

async def run_llm(prompt=None, image_path=None):

    try:

        result = await asyncio.to_thread(
            ask_local_llm,
            prompt,
            image_path
        )

        polished = polish_output(result)

        log("FINAL OUTPUT", polished)

        return polished

    except Exception:

        error = traceback.format_exc()

        log("LLM ERROR", error)

        return "Error generating response."