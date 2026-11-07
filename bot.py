import os
import telebot
import threading
from flask import Flask

TOKEN = os.environ.get("BOT_TOKEN")
bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)
users = {}

def send_start(message):
    chat_id = message.chat.id
    users[chat_id] = "ask_name"
    bot.reply_to(message, "نبدأ من الأول ❤️\nأهلاً أهلاً بأحلى ناس في الدنيا 🥰\nوحشتوني أوي والله\nقولي بقى مين اللي معايا؟\nشيماء ولا ياسين ولا أسر ولا سليم؟")

@bot.message_handler(commands=['start', 'restart'])
def start(message):
    send_start(message)

@bot.message_handler(func=lambda m: True)
def reply(message):
    chat_id = message.chat.id
    text = message.text.lower().strip()

    if text in ["restart", "ريستارت", "نبدأ من الاول", "نبدا من الاول", "ابدأ من الأول", "ابدا من الاول", "من الاول", "نبدأ من الأول"]:
        send_start(message)
        return

    state = users.get(chat_id, "ask_name")

    if state == "ask_name":
        if "ياسين" in text:
            users[chat_id] = "wait_ok"
            bot.reply_to(message, "ياسينووو حبيب قلبي ❤️🥰\nازيك يا بطل عامل ايه؟ يا رب تكون بخير والف مليون سلامة على رجلك يا حبيبي، ربنا يشفيك ويقومك بالسلامة\nعايزك تتمرن كويس يا وحش وذاكر كويس عشان انت في ثالثة اعدادي وقدها وقدود، انا واثق فيك يا بطل 💪")
        elif "شيماء" in text:
            users[chat_id] = "wait_ok"
            bot.reply_to(message, "شيماء حبيبتي ❤️🥰\nازيك يا قمر عاملة ايه؟ وحشتيني أوي\nعايزك تاخدي بالك من سامح، ده بيحبك جدا والله ❤️ وربنا يقويكي ويعينك على ولادك يا بطلة، خلي بالك منهم دول حبايب قلبي كلهم")
        elif "اسر" in text or "أسر" in text:
            users[chat_id] = "wait_ok"
            bot.reply_to(message, "أسووور حبيب قلبي ❤️🥰\nازيك يا بطل عامل ايه؟ وحشتني يا جميل\nنام كويس يا حبيبي وكل كويس، وركز في مذاكرتك وقرآنك، انت شاطر وجميل وانا فخور بيك أوي ❤️")
        elif "سليم" in text:
            users[chat_id] = "wait_ok"
            bot.reply_to(message, "سليمووو حبيب قلبي ❤️🥰\nازيك يا بطل عامل ايه؟ وحشتني أوي\nذاكر كويس يا حبيبي، وكل اصحابك في الهوم سكولينج بيحبوك أوي وبيقولوا سليم ده أحلى واحد فينا 🥰")
        else:
            bot.reply_to(message, "قولي يا حبيبي انت مين؟ شيماء ولا ياسين ولا أسر ولا سليم؟ 🥰")
        return

    if state == "wait_ok":
        if "تمام" in text or "هنعمل" in text or "حاضر" in text or "ماشي" in text:
            bot.reply_to(message, "انا كنت متأكد ان انتو هتعملوا كده ❤️\nعشان انتو أحلى ولاد في الدنيا وشاطرين وحنينين، ربنا يخليكو ليا يا حبايب قلبي 🥰")
            users[chat_id] = "done"
        else:
            bot.reply_to(message, "قولي تمام هنعمل كده يا حبيبي لو هتعمل اللي قولتهولك ❤️🥰")
        return

    if state == "done":
        if "صباح الخير" in text:
            bot.reply_to(message, "صباح الفل والياسمين على أحلى واحد في الدنيا ❤️🥰 عامل ايه يا حبيبي؟")
        elif "ازيك" in text or "عامل ايه" in text:
            bot.reply_to(message, "الحمد لله تمام يا حبيبي طول ما انتو بخير ❤️ انت عامل ايه؟ وحشتني")
        elif "بحبك" in text:
            bot.reply_to(message, "وانا بموت فيك يا حبيب قلبي ❤️❤️❤️")
        else:
            bot.reply_to(message, "نورتني يا حبيبي ❤️ لو عايز نبدأ من الأول اكتب نبدأ من الاول")
        return

@app.route('/')
def home():
    return "البوت شغال تمام!"

def run_bot():
    bot.infinity_polling()

if __name__ == "__main__":
    threading.Thread(target=run_bot).start()
    app.run(host="0.0.0.0", port=10000)
