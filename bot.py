import telebot

TOKEN = "حط_التوكن_بتاعك_هنا"
bot = telebot.TeleBot(TOKEN)

MY_NUMBER = "01067654540"
MY_WHATSAPP = "https://wa.me/201067654540"

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "اهلا وسهلا بيك في بوت سامح 👋\nانا معاك، اسألني اي حاجة وهرد عليك كتابة وصوت\nولو قولت ارسملي هبعتلك صورة\n\nعشان تتواصل مع صاحب البوت دوس /contact")

@bot.message_handler(commands=['contact'])
def contact(message):
    bot.reply_to(message, f"اهلا وسهلا بيك في بوت سامح ❤️\n\nللتواصل مع صاحب البوت:\n📞 تليفون: {MY_NUMBER}\n💬 واتساب: {MY_WHATSAPP}\n\nاتصل في اي وقت واحنا في خدمتك")

@bot.message_handler(content_types=['voice'])
def voice_reply(message):
    bot.reply_to(message, "اهلا وسهلا بيك في بوت سامح، سمعت رسالتك الصوتية، اتفضل اكتبلي اللي انت عايزه وانا هرد عليك")

@bot.message_handler(func=lambda m: True)
def all_messages(message):
    text = message.text.lower() if message.text else ""

    if "ارسم" in text or "صورة" in text or "رسم" in text:
        bot.reply_to(message, "اهلا وسهلا بيك في بوت سامح، حاضر هرسملك، قولي عايز ترسم ايه بالظبط؟")

    elif "سعر" in text or "بكام" in text or "تكلفة" in text:
        bot.reply_to(message, f"اهلا وسهلا بيك في بوت سامح، الاسعار بتختلف على حسب شغلك، كلمنا على {MY_NUMBER} وهنقولك كل التفاصيل")

    elif "سلام" in text or "هلا" in text or "ازيك" in text or "اهلا" in text:
        bot.reply_to(message, "اهلا وسهلا بيك في بوت سامح، نورتنا ❤️ اسألني اي حاجة")

    else:
        bot.reply_to(message, "اهلا وسهلا بيك في بوت سامح، فهمتك، قولي بقى عايز ايه بالظبط؟ ولو عايز تكلم صاحب البوت دوس /contact")

print("البوت شغال...")
bot.infinity_polling()
