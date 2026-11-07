import os
import telebot
import threading
from flask import Flask

TOKEN = os.environ.get("BOT_TOKEN")
bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)
users = {}

def send_restart(message):
    chat_id = message.chat.id
    users[chat_id] = "restart_wait"
    bot.reply_to(message, "تمام ❤️\nهنبدأ من الأول خالص\nقول نبدأ عشان نبدأ 🥰")

def send_ask_name(message):
    chat_id = message.chat.id
    users[chat_id] = "ask_name"
    bot.reply_to(message, "نبدأ من الأول ❤️\nأهلاً أهلاً بأحلى ناس في الدنيا 🥰\nوحشتوني أوي والله\nقولي بقى مين اللي معايا؟\nشيماء ولا ياسين ولا أسر ولا سليم ولا سامح؟")

@bot.message_handler(commands=['start', 'restart'])
def start(message):
    send_restart(message)

@bot.message_handler(func=lambda m: True)
def reply(message):
    chat_id = message.chat.id
    text = message.text.lower().strip()

    # لو قال ريستارت او من الاول -> يبدأ من الأول خالص
    if text in ["restart", "ريستارت", "من الاول", "من الأول", "نبدأ من الاول", "نبدا من الاول", "ابدأ من الأول", "ابدا من الاول", "نبدأ من الأول"]:
        send_restart(message)
        return

    state = users.get(chat_id, "restart_wait")

    # هو مستني كلمة نبدأ بعد الريستارت
    if state == "restart_wait":
        if "نبدأ" in text or "نبدا" in text or "يلا" in text or "تمام" in text or "ابدأ" in text or "ابدا" in text:
            send_ask_name(message)
        else:
            bot.reply_to(message, "قول نبدأ عشان نبدأ من الأول ❤️🥰")
        return

    # بنشوف الاسم حتى لو في جملة طويلة
    found_name = None
    if "ياسين" in text:
        found_name = "ياسين"
    elif "شيماء" in text:
        found_name = "شيماء"
    elif "اسر" in text or "أسر" in text:
        found_name = "اسر"
    elif "سليم" in text:
        found_name = "سليم"
    elif "سامح" in text:
        found_name = "سامح"

    if state == "ask_name":
        if found_name == "ياسين":
            users[chat_id] = "wait_ok"
            bot.reply_to(message, "ياسينووو حبيب قلبي ❤️🥰\nازيك يا بطل عامل ايه؟ يا رب تكون بخير والف مليون سلامة على رجلك يا حبيبي، ربنا يشفيك ويقومك بالسلامة\nعايزك تحافظ على صلاتك يا حبيبي، صلي في وقتها وادعي ربنا يشفيك ويوفقك ❤️\nواتمرن كويس يا وحش وذاكر كويس عشان انت في ثالثة اعدادي وقدها وقدود، انا واثق فيك يا بطل 💪")
        elif found_name == "شيماء":
            users[chat_id] = "wait_ok"
            bot.reply_to(message, "شيماء حبيبتي ❤️🥰\nازيك يا قمر عاملة ايه؟ وحشتيني أوي\nعايزك تحافظي على صلاتك يا حبيبتي، صلي وادعي لولادك ربنا يحفظهم ويبارك فيهم ❤️\nوعايزك تاخدي بالك من سامح، ده بيحبك جدا والله ❤️ وربنا يقويكي ويعينك على ولادك يا بطلة، خلي بالك منهم دول حبايب قلبي كلهم")
        elif found_name == "اسر":
            users[chat_id] = "wait_ok"
            if "مش عايز" in text or "مش عاوز" in text or "مدرسة" in text:
                bot.reply_to(message, "أسووور حبيب قلبي ❤️🥰\nمالك يا بطل مش عايز تروح المدرسة ليه؟\nمعلش يا حبيبي انا عارف انك زهقت، بس انت شاطر وجميل، روح وجرب وهتتبسط، ولو حصل حاجة قولي\nوعايزك تحافظ على صلاتك يا حبيبي، صلي في وقتها، وركز في مذاكرتك وقرآنك، انا فخور بيك أوي ❤️")
            else:
                bot.reply_to(message, "أسووور حبيب قلبي ❤️🥰\nازيك يا بطل عامل ايه؟ وحشتني يا جميل\nعايزك تحافظ على صلاتك يا حبيبي، صلي في وقتها وادعي ربنا يوفقك ❤️\nنام كويس يا حبيبي وكل كويس، وركز في مذاكرتك وقرآنك، انت شاطر وجميل وانا فخور بيك أوي ❤️")
        elif found_name == "سليم":
            users[chat_id] = "wait_ok"
            bot.reply_to(message, "سليمووو حبيب قلبي ❤️🥰\nازيك يا بطل عامل ايه؟ وحشتني أوي\nعايزك تحافظ على صلاتك يا حبيبي، صلي في وقتها وربنا هيباركلك ويوفقك ❤️\nذاكر كويس يا حبيبي، وكل اصحابك في الهوم سكولينج بيحبوك أوي وبيقولوا سليم ده أحلى واحد فينا 🥰")
        elif found_name == "سامح":
            users[chat_id] = "done"
            bot.reply_to(message, "سامح حبيب قلبي ❤️🥰\nازيك يا أبو العيال يا غالي؟ وحشتني أوي والله\nعايزك تحافظ على صلاتك يا حبيبي، صلي في وقتها وادعي لولادك ❤️\nانت عامل ايه؟ طمني عليك، ولادك بيحبوك أوي ❤️")
        else:
            if "عامل ايه" in text or "ازيك" in text:
                bot.reply_to(message, "الحمد لله تمام يا حبيبي طول ما انت بخير ❤️\nانت عامل ايه؟ وحشتني\nقولي بقى انت مين؟ شيماء ولا ياسين ولا أسر ولا سليم ولا سامح؟ 🥰")
            elif "وحشتني" in text or "وحشتيني" in text:
                bot.reply_to(message, "وانت كمان وحشتني أوي أوي ❤️🥰\nقولي بقى انت مين عشان اعرف اتكلم معاك؟ شيماء ولا ياسين ولا أسر ولا سليم؟")
            else:
                bot.reply_to(message, "قولي يا حبيبي انت مين؟ شيماء ولا ياسين ولا أسر ولا سليم ولا سامح؟ 🥰")
        return

    if state == "wait_ok":
        if "تمام" in text or "هنعمل" in text or "حاضر" in text or "ماشي" in text:
            bot.reply_to(message, "انا كنت متأكد ان انتو هتعملوا كده ❤️\nعشان انتو أحلى ولاد في الدنيا وشاطرين وحنينين، ربنا يخليكو ليا يا حبايب قلبي 🥰")
            users[chat_id] = "done"
        else:
            bot.reply_to(message, "قولي تمام هنعمل كده يا حبيبي لو هتعمل اللي قولتهولك ❤️🥰")
        return

    if state == "done":
        if found_name:
            users[chat_id] = "ask_name"
            reply(message)
            return
        if "صباح الخير" in text:
            bot.reply_to(message, "صباح الفل والياسمين على أحلى واحد في الدنيا ❤️🥰 عامل ايه يا حبيبي؟")
        elif "ازيك" in text or "عامل ايه" in text:
            bot.reply_to(message, "الحمد لله تمام يا حبيبي طول ما انتو بخير ❤️ انت عامل ايه؟ وحشتني")
        elif "بحبك" in text:
            bot.reply_to(message, "وانا بموت فيك يا حبيب قلبي ❤️❤️❤️")
        elif "وحشتني" in text:
            bot.reply_to(message, "وانت كمان وحشتني أوي ❤️🥰")
        else:
            bot.reply_to(message, "نورتني يا حبيبي ❤️ لو عايز نبدأ من الأول اكتب ريستارت")
        return

@app.route('/')
def home():
    return "البوت شغال تمام!"

def run_bot():
    bot.infinity_polling()

if __name__ == "__main__":
    threading.Thread(target=run_bot).start()
    app.run(host="0.0.0.0", port=10000)
