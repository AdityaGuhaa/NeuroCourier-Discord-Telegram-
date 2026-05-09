import os
import time
import re
import traceback
from datetime import datetime

from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, ContextTypes, filters
from telegram.constants import ParseMode

from llm_backend import run_llm, log

from dotenv import load_dotenv
load_dotenv()
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

# ================= CONFIG =================

DATA_DIR = "data"
os.makedirs(DATA_DIR, exist_ok=True)


# ================= MARKDOWN ESCAPE =================

def escape_markdown(text: str):
    escape_chars = r"_*[]()~`>#+-=|{}.!\\"
    return re.sub(f"([{re.escape(escape_chars)}])", r"\\\1", text)


# ================= MESSAGE SPLITTER =================

def split_message(text, limit=4000):
    chunks = []
    while len(text) > limit:
        split_at = text.rfind('\n', 0, limit)
        if split_at == -1:
            split_at = limit
        chunks.append(text[:split_at])
        text = text[split_at:].lstrip('\n')
    chunks.append(text)
    return chunks


# ================= TELEGRAM SAFE SEND =================

async def safe_send_chunks(update, thinking_msg, text):
    chunks = split_message(text)

    # Edit the "Thinking..." message with the first chunk
    try:
        escaped = escape_markdown(chunks[0])
        await thinking_msg.edit_text(escaped, parse_mode=ParseMode.MARKDOWN_V2)
    except Exception:
        await thinking_msg.edit_text(chunks[0])

    # Send remaining chunks as new messages
    for chunk in chunks[1:]:
        try:
            escaped = escape_markdown(chunk)
            await update.message.reply_text(escaped, parse_mode=ParseMode.MARKDOWN_V2)
        except Exception:
            await update.message.reply_text(chunk)


# ================= TEXT HANDLER =================

async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text
    log("TELEGRAM RECEIVED", user_message)

    thinking_msg = await update.message.reply_text("Thinking...")

    reply = await run_llm(prompt=user_message)

    await safe_send_chunks(update, thinking_msg, reply)


# ================= IMAGE HANDLER =================

async def handle_image(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        photo = update.message.photo[-1]
        file = await context.bot.get_file(photo.file_id)

        timestamp = int(time.time())
        file_path = os.path.join(DATA_DIR, f"telegram_image_{timestamp}.jpg")
        await file.download_to_drive(file_path)

        # Use caption if provided, otherwise default prompt
        caption = update.message.caption if update.message.caption else "Analyze this image."

        log("TELEGRAM IMAGE", file_path)

        thinking_msg = await update.message.reply_text("Analyzing image...")

        reply = await run_llm(prompt=caption, image_path=file_path)

        await safe_send_chunks(update, thinking_msg, reply)

    except Exception:
        error = traceback.format_exc()
        log("TELEGRAM IMAGE ERROR", error)
        await update.message.reply_text("Image processing error.")


# ================= MAIN =================

def main():
    print("\n" + "=" * 60)
    print("NeuroCourier Telegram Bot Starting")
    print("=" * 60)

    app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()

    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))
    app.add_handler(MessageHandler(filters.PHOTO, handle_image))

    print("Telegram bot is LIVE")
    print("=" * 60)

    app.run_polling()


# ================= ENTRY =================

if __name__ == "__main__":
    main()