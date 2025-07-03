import os
import requests
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes

# Configurazione semplice
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
DEEPSEEK_API_KEY = os.getenv('DEEPSEEK_API_KEY')

async def rispondi(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Prendi il messaggio dell'utente
    messaggio = update.message.text
    
    # Chiama DeepSeek
    headers = {"Authorization": f"Bearer {DEEPSEEK_API_KEY}"}
    data = {
        "model": "deepseek-chat",
        "messages": [{"role": "user", "content": messaggio}]
    }
    
    try:
        risposta = requests.post(
            "https://api.deepseek.com/chat/completions",
            json=data,
            headers=headers
        ).json()
        
        # Estrai il testo della risposta
        testo_risposta = risposta['choices'][0]['message']['content']
        await update.message.reply_text(testo_risposta)
    
    except Exception as e:
        await update.message.reply_text(f"❌ Errore: {str(e)}")

# Avvio del bot
app = Application.builder().token(TELEGRAM_TOKEN).build()
app.add_handler(MessageHandler(filters.TEXT, rispondi))
print("🟢 BOT AVVIATO!")
app.run_polling()
