import os
import requests
import logging
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes

# Configurazione logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Carica le variabili d'ambiente
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
DEEPSEEK_API_KEY = os.getenv('DEEPSEEK_API_KEY')

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text
    logger.info(f"Messaggio ricevuto: {user_message}")
    
    # Prepara la chiamata all'API di DeepSeek
    headers = {
        "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": "deepseek-chat",
        "messages": [
            {"role": "system", "content": "Sei un assistente utile e preciso."},
            {"role": "user", "content": user_message}
        ],
        "temperature": 0.7,
        "max_tokens": 2000
    }
    
    try:
        # Effettua la chiamata API
        response = requests.post(
            "https://api.deepseek.com/chat/completions",
            headers=headers,
            json=payload,
            timeout=30
        )
        
        if response.status_code == 200:
            response_data = response.json()
            if 'choices' in response_data and len(response_data['choices']) > 0:
                bot_response = response_data['choices'][0]['message']['content']
                await update.message.reply_text(bot_response)
            else:
                await update.message.reply_text("🤔 Non ho ricevuto una risposta valida")
        else:
            error_msg = f"Errore API: {response.status_code} - {response.text}"
            logger.error(error_msg)
            await update.message.reply_text("⚠️ Errore nel servizio, riprova più tardi")
            
    except Exception as e:
        logger.error(f"Eccezione: {str(e)}")
        await update.message.reply_text("😢 Si è verificato un errore imprevisto")

def main():
    logger.info("Avvio del bot...")
    application = Application.builder().token(TELEGRAM_TOKEN).build()
    
    # Aggiungi handler per i messaggi
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    logger.info("Bot in ascolto...")
    application.run_polling()

if __name__ == '__main__':
    main()
