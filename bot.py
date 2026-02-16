import asyncio
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, ContextTypes, filters

#CONFIG
TELEGRAM_BOT_TOKEN = "8544832281:AAGGo5kbtSCW-TgZizRjRz6omRmGfaZM3T0"

USE_LOCAL_LLM = True   # True = Ollama, False = Gemini

#OLLAMA SETUP
def ask_local_llm(prompt):
    import ollama
    response = ollama.chat(
        model="qwen3-vl:8b",  #you can use any other local LLM here
        messages=[{"role": "user", "content": prompt}]
    )
    return response['message']['content']

#GEMINI SETUP
def ask_gemini(prompt):
    import google.generativeai as genai

    genai.configure(api_key="PASTE_YOUR_GEMINI_API_KEY") #you can get your gemini api key from https://aistudio.google.com/app/apikey

    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(prompt)

    return response.text

#TELEGRAM HANDLER
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user_message = update.message.text

    print(f"User: {user_message}")

    try:
        if USE_LOCAL_LLM:
            reply = ask_local_llm(user_message)
        else:
            reply = ask_gemini(user_message)

    except Exception as e:
        reply = f"Error: {str(e)}"

    print(f"Bot: {reply}")

    await update.message.reply_text(reply)


#MAIN
def main():

    app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()

    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("Bot is running...")

    app.run_polling()


if __name__ == "__main__":
    main()

