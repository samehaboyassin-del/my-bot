import os
from flask import Flask
import threading
import telebot

TOKEN = os.environ.get("BOT_TOKEN", "")

bot = telebot.TeleBot(TOKEN)

app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is running!"

def run_flask():
    app.run(host='0.0.0.0', port=10000)

@bot.message_handler(commands=['start'])
def start(m):
    bot.reply_to(m, "اهلا بيك في بوت سامح ❤️\nعامل ايه؟ نورتنا والله")

@bot.message_handler(func=lambda m: True)
def reply(m):
    bot.reply_to(m, f"وصلتني رسالتك: {m.text} ❤️")

if __name__ == "__main__":
    threading.Thread(target=run_flask).start()
    print("البوت شغال...")
    bot.infinity_polling()
