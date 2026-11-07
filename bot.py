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
    app.run(host="0.0.0.0", port=10000)

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "❤️ اهلا بيك في بوت سامح\nعامل ايه؟ نورتنا والله\nجرب تقولي: ازيك - مساء الخير - صباح الخير - شكرا - بحبك")

@bot.message_handler(func=lambda m: True)
def reply(message):
    text = message.text.lower().strip() if message.text else ""

    if "ازيك" in text or "عامل ايه" in text or "اخبارك" in text:
        msg = "الحمد لله زي الفل ❤️ وانت عامل ايه؟ طمني عليك"
    elif "صباح الخير" in text or "صباح" in text:
        msg = "صباح النور والهنا ☀️ يومك جميل ان شاء الله"
    elif "مساء الخير" in text or "مساء" in text:
        msg = "مساء النور يا غالي 🌙 نورت البوت والله"
    elif "سلام" in text or "السلام" in text:
        msg = "وعليكم السلام ورحمة الله وبركاته ❤️"
    elif "شكرا" in text or "شكراً" in text:
        msg = "العفو يا حبيبي ❤️ ده واجبي، انت تأمر"
    elif "بحبك" in text or "حبيبي" in text:
        msg = "وانا بحبك اكتر والله ❤️❤️ انت حبيب قلبي"
    elif "اسمك ايه" in text or "انت مين" in text:
        msg = "انا بوت سامح 😎 صاحبك الجديد، معمول مخصوص عشانك"
    elif "بتعمل ايه" in text:
        msg = "قاعد مستنيك تكلمني 😂 مش بعمل حاجة من غيرك"
    elif "ههه" in text or "😂" in text:
        msg = "😂😂 ضحكتك حلوة والله، ضحكني معاك"
    elif "باي" in text:
        msg = "هتوحشني والله 🥺 متتأخرش عليا"
    else:
        msg = f"وصلتني رسالتك: {message.text} ❤️\nجرب تقولي: ازيك - صباح الخير - مساء الخير"

    bot.reply_to(message, msg)

if __name__ == "__main__":
    threading.Thread(target=run_flask, daemon=True).start()
    print("Bot is running...")
    bot.infinity_polling()
