import os
import telebot
import threading
from flask import Flask

TOKEN = os.environ.get("BOT_TOKEN")
bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

# بنحفظ هنا كل واحد وصل لفين
users = {}

@bot.message_handler(commands=['start', 'restart'])
def start(message):
    chat_id = message.chat.id
    users[chat_id] = "ask_name"
    bot.reply_to(message, "أهلاً بيك ❤️\nخلينا نبدأ من الأول\nمين اللي معايا؟\nشيماء ولا ياسين ولا أسر ولا سليم؟")

@bot.message_handler(func=lambda m: True)
def reply(message):
    chat_id = message.chat.id
    text = message.text.lower()
    state = users.get(chat_id, "ask_name")

    # لو لسه بنسأل عن الاسم
    if state == "ask_name":
        if "ياسين" in text:
            users[chat_id] = "wait_ok"
            bot.reply_to(message, "ازيك يا ياسين عامل ايه يا رب تكون بخير والف سلامة على رجلك ❤️\nاتمرن كويس يا ياسين وذاكر كويس عشان انت في ثالثة اعدادي")
        elif "شيماء" in text:
            users[chat_id] = "wait_ok"
            bot.reply_to(message, "ازيك يا شيماء ❤️\nعايزك تاخدي بالك من سامح وبيحبك جدا وربنا يقويكي ويعينك على ولادك خلي بالك منهم")
        elif "اسر" in text or "أسر" in text:
            users[chat_id] = "wait_ok"
            bot.reply_to(message, "ازيك يا أسر ❤️\nنام كويس يا أسر وكل كويس وركز في مذاكرتك وقرآنك")
        elif "سليم" in text:
            users[chat_id] = "wait_ok"
            bot.reply_to(message, "ازيك يا سليم ❤️\nذاكر كويس وكل اصحابك في الهوم سكولينج بيحبوك")
        else:
            bot.reply_to(message, "قولي اسمك، انت شيماء ولا ياسين ولا أسر ولا سليم؟")
        return

    # لو هو رد وقال تمام هنعمل كده
    if state == "wait_ok":
        if "تمام" in text or "هنعمل" in text or "حاضر" in text or "ماشي" in text:
            bot.reply_to(message, "انا كنت متأكد ان انتو هتعملوا كده ❤️\nربنا يخليكو ليا")
            users[chat_id] = "done"
        elif "صباح الخير" in text:
            bot.reply_to(message, "صباح الفل ❤️ عامل ايه؟")
        elif "مساء الخير" in text:
            bot.reply_to(message, "مساء الجمال ❤️")
        else:
            bot.reply_to(message, "قولي تمام هنعمل كده لو هتعمل اللي قولتهولك ❤️")
        return

    # لو خلص خالص
    if state == "done":
        if "صباح الخير" in text:
            bot.reply_to(message, "صباح الفل ❤️")
        elif "ازيك" in text or "عامل ايه" in text:
            bot.reply_to(message, "الحمد لله تمام، وانت عامل ايه؟")
        else:
            bot.reply_to(message, "نورتني ❤️ لو عايز نبدأ من الأول ابعت /restart")
        return

@app.route('/')
def home():
    return "البوت شغال تمام!"

def run_bot():
    bot.infinity_polling()

if __name__ == "__main__":
    threading.Thread(target=run_bot).start()
    app.run(host="0.0.0.0", port=10000)
