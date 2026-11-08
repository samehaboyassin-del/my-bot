import telebot
import os

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
bot = telebot.TeleBot(TOKEN)

MY_NUMBER = "01067654540"
MY_WHATSAPP = "https://wa.me/201067654540"

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "اهلا وسهلا بيك في بوت سامح 👋\nانا معاك، اسألني اي حاجة وهرد عليك\n\nعشان تشوف خدماتنا دوس /services\nعشان تتواصل مع صاحب البوت دوس /contact")

@bot.message_handler(commands=['contact'])
def contact(message):
    bot.reply_to(message, "اهلا وسهلا بيك في بوت سامح ❤️\n\nللتواصل مع صاحب البوت:\n📞 تليفون: 01067654540\n💬 واتساب:\nhttps://wa.me/201067654540\n\nاتصل في اي وقت واحنا في خدمتك")

@bot.message_handler(commands=['services'])
def services(message):
    bot.reply_to(message, "اهلا وسهلا بيك في بوت سامح ❤️\n\nخدماتنا:\n1️⃣ تصميم بوت تليجرام للمحلات والشركات\n2️⃣ بوت واتساب للرد على العملاء\n3️⃣ بوت لعرض المنتجات والاسعار\n4️⃣ بوت لحجز المواعيد والطلبات\n5️⃣ بوت ذكاء اصطناعي بيرد كتابة وصوت\n\nعشان تطلب خدمة دوس /contact\nوكلمنا على 01067654540")

@bot.message_handler(content_types=['voice'])
def voice_reply(message):
    bot.reply_to(message, "اهلا وسهلا بيك في بوت سامح، سمعت رسالتك الصوتية، اتفضل اكتبلي اللي انت عايزه وانا هرد عليك")

@bot.message_handler(func=lambda m: True)
def all_messages(message):
    text = message.text.lower() if message.text else ""

    if "ارسم" in text or "صورة" in text or "رسم" in text:
        bot.reply_to(message, "اهلا وسهلا بيك في بوت سامح، حاضر هرسملك، قولي عايز ترسم ايه بالظبط؟")

    elif "خدمات" in text or "خدمة" in text or "بتعمل ايه" in text or "ايه الخدمات" in text:
        bot.reply_to(message, "اهلا وسهلا بيك في بوت سامح ❤️\n\nخدماتنا:\n1️⃣ تصميم بوت تليجرام للمحلات والشركات\n2️⃣ بوت واتساب للرد على العملاء\n3️⃣ بوت لعرض المنتجات والاسعار\n4️⃣ بوت لحجز المواعيد والطلبات\n\nعشان تطلب دوس /contact")

    elif "سعر" in text or "بكام" in text or "تكلفة" in text:
        bot.reply_to(message, "اهلا وسهلا بيك في بوت سامح، الاسعار بتختلف على حسب شغلك، كلمنا على 01067654540 وهنقولك كل التفاصيل")

    elif "سلام" in text or "هلا" in text or "ازيك" in text or "اهلا" in text:
        bot.reply_to(message, "اهلا وسهلا بيك في بوت سامح، نورتنا ❤️ اسألني اي حاجة، ولو عايز تشوف خدماتنا دوس /services")

    else:
        bot.reply_to(message, "اهلا وسهلا بيك في بوت سامح، فهمتك، قولي بقى عايز ايه بالظبط؟ ولو عايز تشوف خدماتنا دوس /services ولو عايز تكلم صاحب البوت دوس /contact")

print("البوت شغال...")
bot.infinity_polling()
