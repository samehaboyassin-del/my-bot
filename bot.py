import os
from flask import Flask
import threading
import telebot

TOKEN = os.environ.get("BOT_TOKEN", "")
bot = telebot.TeleBot(TOKEN)

app = Flask(__name__)

@app.route("/")
def home():
    return "Bot is working!"

@bot.message_handler(func=lambda m: True)
def reply(m):
    text = (m.text or "").lower()

    if "مساء" in text or "صباح" in text or "سلام" in text or "hi" in text or "hello" in text:
        bot.reply_to(m, "أهلاً بيك في محلنا ❤️ تحب تحجز اوردر ولا عندك مشكلة؟")
    elif "احجز" in text or "حجز" in text or "اطلب" in text:
        bot.reply_to(m, "تمام، تحب تطلب ايه؟ عندنا عرض: 350 بدل 450، ايه اللون والمقاس اللي عايزه؟")
    elif "مشك" in text or "غلط" in text or "مشكل" in text:
        bot.reply_to(m, "فهمتك، فيه مشكلة في الاوردر ❤️ انا هحولك لخدمة العملاء، هما هيكلموك حالا ويساعدوك")
    else:
        bot.reply_to(m, "فهمتك ❤️ ممكن توضح اكتر؟ تحب تحجز ولا عندك مشكلة؟")

def run_bot():
    bot.infinity_polling()

threading.Thread(target=run_bot, daemon=True).start()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
