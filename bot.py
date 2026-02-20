import os
import time
import re
import traceback
from datetime import datetime

from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, ContextTypes, filters
from telegram.constants import ParseMode

# Import shared LLM backend
from llm_backend import run_llm, log


# ================= CONFIG =================

TELEGRAM_BOT_TOKEN = "Put Your Telegram bot API here"

DATA_DIR = "data"

os.makedirs(DATA_DIR, exist_ok=True)


# ================= MARKDOWN ESCAPE =================

def escape_markdown(text: str):

    escape_chars = r"_*[]()~`>#+-=|{}.!\\"
    return re.sub(f"([{re.escape(escape_chars)}])", r"\\\1", text)


# ================= TELEGRAM SAFE SEND =================

async def safe_edit_message(message, text):

    try:

        escaped = escape_markdown(text)

        await message.edit_text(
            escaped,
            parse_mode=ParseMode.MARKDOWN_V2
        )

        log("TELEGRAM SENT", "Markdown message sent")

    except Exception:

        await message.edit_text(text)

        log("TELEGRAM SENT", "Plain text message sent")


# ================= TEXT HANDLER =================

async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user_message = update.message.text

    log("TELEGRAM RECEIVED", user_message)

    thinking_msg = await update.message.reply_text("Thinking...")

    reply = await run_llm(
        prompt=user_message
    )

    await safe_edit_message(thinking_msg, reply)


# ================= IMAGE HANDLER =================

async def handle_image(update: Update, context: ContextTypes.DEFAULT_TYPE):

    try:

        photo = update.message.photo[-1]

        file = await context.bot.get_file(photo.file_id)

        timestamp = int(time.time())

        file_path = os.path.join(
            DATA_DIR,
            f"telegram_image_{timestamp}.jpg"
        )

        await file.download_to_drive(file_path)

        caption = update.message.caption

        log("TELEGRAM IMAGE", f"{file_path}")

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

        log("TELEGRAM IMAGE ERROR", error)

        await update.message.reply_text(
            "Image processing error."
        )


# ================= MAIN =================

def main():

    print("\n" + "=" * 60)
    print("NeuroCourier Telegram Bot Starting")
    print("=" * 60)

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

    print("Telegram bot is LIVE")
    print("=" * 60)

    app.run_polling()


# ================= ENTRY =================

if __name__ == "__main__":
    main()