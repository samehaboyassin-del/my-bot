import os
import telebot
from flask import Flask

TOKEN = os.environ.get("BOT_TOKEN")
bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

# رسالة البداية - لما يبدأ من الأول
@bot.message_handler(commands=['start', 'restart'])
def start(message):
    bot.reply_to(message, "أهلاً بيك في بوت سامح ❤️\nخلينا نبدأ من الأول\nانت عامل ايه؟")

# ردود التحيات
@bot.message_handler(func=lambda m: True)
def reply(message):
    text = message.text.lower()

    if "صباح الخير" in text:
        bot.reply_to(message, "صباح الفل ❤️ عامل ايه؟")
    elif "مساء الخير" in text:
        bot.reply_to(message, "مساء الجمال ❤️ عامل ايه؟")
    elif "ازيك" in text or "عامل ايه" in text:
        bot.reply_to(message, "الحمد لله تمام، وانت عامل ايه؟")
    elif "الحمد لله" in text:
        bot.reply_to(message, "دايماً يارب ❤️")
    elif "بقولك ايه" in text:
        bot.reply_to(message, "قول يا معلم سامعك 👂")
    elif "شكرا" in text:
        bot.reply_to(message, "العفو يا صاحبي ❤️")
    elif "بحبك" in text:
        bot.reply_to(message, "وانا كمان بحبك ❤️")
    else:
        bot.reply_to(message, "مش فاهمك، جرب تقولي ازيك او صباح الخير")

@app.route('/')
def home():
    return "البوت شغال تمام!"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
