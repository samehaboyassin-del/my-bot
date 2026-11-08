import os
import io
import telebot
from google import genai
from gtts import gTTS
from PIL import Image

TELEGRAM_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN") or os.getenv("BOT_TOKEN") or os.getenv("TELEGRAM_TOKEN")
GEMINI_KEY = os.getenv("GEMINI_API_KEY")

client = genai.Client(api_key=GEMINI_KEY)
bot = telebot.TeleBot(TELEGRAM_TOKEN)

TEXT_MODELS = ["gemini-3.5-flash-lite", "gemini-3.8-flash", "gemini-3-flash-preview"]
IMAGE_MODEL = "gemini-3-pro-image-preview"

IMAGE_WORDS = ["ارسم", "ارسملي", "صورة", "صوره", "تخيل", "اعملي", "رسم", "image", "draw", "picture"]

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "اهلا يا سامح! اسألني اي حاجة وهرد كتابة وصوت، ولو قولت ارسملي هبعتلك صورة")

def is_image_request(text):
    text = text.lower()
    return any(word in text for word in IMAGE_WORDS)

@bot.message_handler(func=lambda m: True)
def ai_reply(message):
    text = message.text

    # لو طلب صورة
    if is_image_request(text):
        bot.send_chat_action(message.chat.id, 'upload_photo')
        bot.reply_to(message, "تمام، برسمهالك دلوقتي... 🎨")
        try:
            response = client.models.generate_content(
                model=IMAGE_MODEL,
                contents=text
            )
            for part in response.candidates[0].content.parts:
                if part.inline_data:
                    img = Image.open(io.BytesIO(part.inline_data.data))
                    img.save("image.png")
                    with open("image.png", "rb") as photo:
                        bot.send_photo(message.chat.id, photo, caption="خلصت، ايه رايك؟ 😍")
                    return
            bot.reply_to(message, "معرفتش ارسمها، جرب توصفها بطريقة تانية")
        except Exception as e:
            bot.reply_to(message, f"توليد الصور مش متاح دلوقتي على المفتاح ده. الخطأ: {e}")
        return

    # لو كلام عادي - كتابة + صوت
    bot.send_chat_action(message.chat.id, 'typing')
    reply_text = ""
    for model_name in TEXT_MODELS:
        try:
            response = client.models.generate_content(model=model_name, contents=text)
            reply_text = response.text
            break
        except Exception:
            continue

    if not reply_text:
        bot.reply_to(message, "جوجل زحمة دلوقتي، جرب تاني بعد دقيقة.")
        return

    bot.reply_to(message, reply_text)
    try:
        bot.send_chat_action(message.chat.id, 'record_voice')
        tts = gTTS(text=reply_text[:4000], lang='ar', slow=False)
        tts.save("voice.mp3")
        with open("voice.mp3", "rb") as voice_file:
            bot.send_voice(message.chat.id, voice_file)
    except Exception:
        pass

bot.polling(none_stop=True, timeout=60)
