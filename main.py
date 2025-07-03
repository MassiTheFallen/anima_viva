import os
import asyncio
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, ContextTypes, filters

TOKEN = os.getenv("API_KEY")

async def query_chatgpt(message):
    # Simulazione ChatGPT
    await asyncio.sleep(1)
    return f"ChatGPT dice: {message[:30]}..."

async def query_deepseek(message):
    # Simulazione DeepSeek
    await asyncio.sleep(1)
    return f"DeepSeek risponde a: {message[:30]}..."

async def query_gemini(message):
    # Simulazione Gemini
    await asyncio.sleep(1)
    return f"Gemini commenta: {message[:30]}..."

async def orchestrator(message):
    results = await asyncio.gather(
        query_chatgpt(message),
        query_deepseek(message),
        query_gemini(message)
    )
    return "\n\n".join(results)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    response = await orchestrator(text)
    await update.message.reply_text(response)

if __name__ == "__main__":
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))
    app.run_polling()
