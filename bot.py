import os
import telebot
from google import genai

TELEGRAM_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN") or os.getenv("BOT_TOKEN") or os.getenv("TELEGRAM_TOKEN")
GEMINI_KEY = os.getenv("GEMINI_API_KEY")

client = genai.Client(api_key=GEMINI_KEY)
bot = telebot.TeleBot(TELEGRAM_TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "اهلا يا سامح! انا بوت AI، اسألني اي حاجة")

@bot.message_handler(func=lambda m: True)
def ai_reply(message):
    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=message.text
        )
        bot.reply_to(message, response.text)
    except Exception as e:
        bot.reply_to(message, f"الخطأ هو: {e}")

bot.polling(none_stop=True)
