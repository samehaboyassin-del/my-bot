import os
import time
import telebot
from google import genai

TELEGRAM_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN") or os.getenv("BOT_TOKEN") or os.getenv("TELEGRAM_TOKEN")
GEMINI_KEY = os.getenv("GEMINI_API_KEY")

client = genai.Client(api_key=GEMINI_KEY)
bot = telebot.TeleBot(TELEGRAM_TOKEN)

MODELS = ["gemini-3.8-flash", "gemini-3.5-flash-lite", "gemini-3-flash-preview"]

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "اهلا يا سامح! انا بوت AI، اسألني اي حاجة")

@bot.message_handler(func=lambda m: True)
def ai_reply(message):
    last_error = ""
    for model_name in MODELS:
        try:
            response = client.models.generate_content(
                model=model_name,
                contents=message.text
            )
            bot.reply_to(message, response.text)
            return
        except Exception as e:
            last_error = str(e)
            time.sleep(1)
            continue
    bot.reply_to(message, f"جوجل زحمة دلوقتي، جرب تاني بعد دقيقة.")

bot.polling(none_stop=True)
