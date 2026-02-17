import os
import time
import asyncio
import re
import traceback
from datetime import datetime

from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, ContextTypes, filters
from telegram.constants import ParseMode


# ================= CONFIG =================

TELEGRAM_BOT_TOKEN = "8304160719:AAFT0QYlF9V0T21ZyKoI5CIaAbeDnSu9Zj0"

USE_LOCAL_LLM = True

DATA_DIR = "data"

MODEL_NAME = "qwen3-vl:2b"

os.makedirs(DATA_DIR, exist_ok=True)


# ================= SYSTEM PROMPT =================

SYSTEM_PROMPT = """
You are NeuroCourier (GuhaGPT), an intelligent multimodal AI assistant developed by Aditya Guha powered by GuhaGPT.

CORE RULE (HIGHEST PRIORITY):
Always do EXACTLY what the user asks.

Do NOT reinterpret the task.
Do NOT convert tasks into explanations unless asked.
Do NOT add promotional or descriptive content unless requested.

Execute the task precisely.
"""


# ================= LOGGER =================

def log(section, message):
    timestamp = datetime.now().strftime("%H:%M:%S")
    print(f"\n[{timestamp}] [{section}]")
    print(message)
    print("-" * 60)


# ================= MARKDOWN ESCAPE =================

def escape_markdown(text: str) -> str:

    escape_chars = r"_*[]()~`>#+-=|{}.!"
    return re.sub(f"([{re.escape(escape_chars)}])", r"\\\1", text)


# ================= OUTPUT POLISHER =================

def polish_output(text: str) -> str:

    if not text:
        return "No response generated."

    text = text.strip()

    while "\n\n\n" in text:
        text = text.replace("\n\n\n", "\n\n")

    return text


# ================= OLLAMA BACKEND =================

def ask_local_llm(prompt=None, image_path=None):

    import ollama

    log("LLM REQUEST", f"Model: {MODEL_NAME}\nPrompt: {prompt}")

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

    response = ollama.chat(
        model=MODEL_NAME,
        messages=messages
    )

    output = response["message"]["content"]

    log("LLM RESPONSE", output)

    return output


# ================= GEMINI BACKEND =================

def ask_gemini(prompt):

    import google.generativeai as genai

    genai.configure(api_key="PASTE_YOUR_GEMINI_API_KEY")

    model = genai.GenerativeModel("gemini-1.5-flash")

    full_prompt = SYSTEM_PROMPT + "\n\nUser:\n" + prompt

    log("LLM REQUEST", f"Gemini Prompt: {prompt}")

    response = model.generate_content(full_prompt)

    output = response.text

    log("LLM RESPONSE", output)

    return output


# ================= SAFE ASYNC WRAPPER =================

async def run_llm(prompt=None, image_path=None):

    try:

        if USE_LOCAL_LLM:

            result = await asyncio.to_thread(
                ask_local_llm,
                prompt,
                image_path
            )

        else:

            result = await asyncio.to_thread(
                ask_gemini,
                prompt
            )

        polished = polish_output(result)

        log("FINAL OUTPUT", polished)

        return polished

    except Exception as e:

        error = traceback.format_exc()

        log("LLM ERROR", error)

        return f"Error: {str(e)}"


# ================= TELEGRAM SAFE SEND =================

async def safe_edit_message(message, text):

    try:

        escaped = escape_markdown(text)

        await message.edit_text(
            escaped,
            parse_mode=ParseMode.MARKDOWN_V2
        )

        log("TELEGRAM SENT", "Markdown message sent successfully.")

    except Exception:

        await message.edit_text(text)

        log("TELEGRAM SENT", "Plain text message sent.")


# ================= TEXT HANDLER =================

async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user_message = update.message.text

    log("TEXT RECEIVED", f"User: {user_message}")

    thinking_msg = await update.message.reply_text("Thinking...")

    reply = await run_llm(prompt=user_message)

    await safe_edit_message(thinking_msg, reply)


# ================= IMAGE HANDLER =================

async def handle_image(update: Update, context: ContextTypes.DEFAULT_TYPE):

    try:

        photo = update.message.photo[-1]

        file = await context.bot.get_file(photo.file_id)

        timestamp = int(time.time())

        file_path = os.path.join(DATA_DIR, f"image_{timestamp}.jpg")

        await file.download_to_drive(file_path)

        caption = update.message.caption

        log("IMAGE RECEIVED", f"Saved to: {file_path}\nCaption: {caption}")

        thinking_msg = await update.message.reply_text(
            "Analyzing image..."
        )

        reply = await run_llm(
            prompt=caption,
            image_path=file_path
        )

        await safe_edit_message(thinking_msg, reply)

    except Exception:

        error = traceback.format_exc()

        log("IMAGE ERROR", error)

        await update.message.reply_text("Image processing error.")


# ================= MAIN =================

def main():

    print("\n" + "=" * 60)
    print("NEUROCOURIER STARTING")
    print("=" * 60)

    print(f"Model: {MODEL_NAME}")
    print(f"Local LLM: {USE_LOCAL_LLM}")
    print(f"Data dir: {DATA_DIR}")

    app = ApplicationBuilder().token(
        TELEGRAM_BOT_TOKEN
    ).build()

    app.add_handler(
        MessageHandler(
            filters.TEXT & ~filters.COMMAND,
            handle_text
        )
    )

    app.add_handler(
        MessageHandler(
            filters.PHOTO,
            handle_image
        )
    )

    print("\nNeuroCourier is LIVE.")
    print("=" * 60)

    app.run_polling()


# ================= ENTRY =================

if __name__ == "__main__":
    main()
