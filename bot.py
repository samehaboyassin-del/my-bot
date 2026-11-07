import os
import telebot
import threading
from flask import Flask

TOKEN = os.environ.get("BOT_TOKEN")
bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

def send_start(message):
    bot.reply_to(message, "أهلاً أهلاً ❤️🥰\nنورت الدنيا كلها والله\nانا مبسوط أوي انك كلمتني\nعامل ايه؟ طمني عليك ❤️")

@bot.message_handler(commands=['start', 'restart'])
def start(message):
    send_start(message)

@bot.message_handler(func=lambda m: True)
def reply(message):
    text = message.text.lower().strip()

    if text in ["restart", "ريستارت", "من الاول", "من الأول", "نبدأ من الاول", "نبدا من الاول", "ابدأ من الأول", "ابدا من الاول", "نبدأ من الأول", "نبدأ", "نبدا"]:
        send_start(message)
        return

    if "صباح الخير" in text or "صباح الفل" in text:
        bot.reply_to(message, "صباح الفل والياسمين على أحلى واحد في الدنيا ❤️🥰\nصباحك زي الفل، عامل ايه النهارده؟")
    elif "مساء الخير" in text or "مساء الفل" in text:
        bot.reply_to(message, "مساء الفل والياسمين ❤️🥰\nنورت، عامل ايه؟ يومك كان عامل ازاي؟")
    elif "ازيك" in text or "عامل ايه" in text or "اخبارك" in text:
        bot.reply_to(message, "الحمد لله تمام يا حبيبي طول ما انت بخير ❤️\nانت عامل ايه؟ طمني عليك، وحشتني والله 🥰")
    elif "بحبك" in text:
        bot.reply_to(message, "وانا بموت فيك يا حبيب قلبي ❤️❤️❤️\nانت من أحلى الناس اللي كلمتني والله 🥰")
    elif "وحشتني" in text or "وحشتيني" in text:
        bot.reply_to(message, "وانت كمان وحشتني أوي أوي ❤️🥰\nانا كنت مستنيك تكلمني والله")
    elif "زعلان" in text or "مخنوق" in text or "متضايق" in text:
        bot.reply_to(message, "مالك يا حبيبي؟ ❤️\nمتزعلش، فضفض معايا، انا سامعك\nكل حاجة هتتحل ان شاء الله، انت بس اهدى وطمني عليك 🥰")
    elif "تعبان" in text or "عيان" in text:
        bot.reply_to(message, "ألف مليون سلامة عليك يا حبيبي ❤️\nربنا يشفيك ويقومك بالسلامة\nارتاح واشرب حاجة دافية، وطمني عليك 🥰")
    elif "تمام" in text or "حاضر" in text or "ماشي" in text:
        bot.reply_to(message, "انا كنت متأكد انك هتعمل كده ❤️\nعشان انت جدع وشاطر، ربنا يخليك 🥰")
    elif "شكرا" in text or "تسلم" in text:
        bot.reply_to(message, "العفو يا حبيب قلبي ❤️\nده واجبي، انت تأمر بس 🥰")
    elif "سلام" in text or "باي" in text or "همشي" in text:
        bot.reply_to(message, "هتوحشني والله ❤️🥰\nخلي بالك من نفسك، وارجع كلمني تاني بسرعة")
    else:
        bot.reply_to(message, "نورتني يا حبيبي ❤️🥰\nانا معاك، قولي عامل ايه؟ او لو عايز نبدأ من الأول اكتب ريستارت")

@app.route('/')
def home():
    return "البوت شغال تمام!"

def run_bot():
    bot.infinity_polling()

if __name__ == "__main__":
    threading.Thread(target=run_bot).start()
    app.run(host="0.0.0.0", port=10000)
