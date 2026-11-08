import os
import io
import asyncio
import requests
import urllib.parse
import telebot
from google import genai
from PIL import Image
from google.genai import types

TELEGRAM_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN") or os.getenv("BOT_TOKEN") or os.getenv("TELEGRAM_TOKEN")
GEMINI_KEY = os.getenv("GEMINI_API_KEY")

client = genai.Client(api_key=GEMINI_KEY, http_options=types.HttpOptions(api_version="v1beta"))
bot = telebot.TeleBot(TELEGRAM_TOKEN)

SYSTEM_PROMPT = """
انت بوت اسمه "بوت سامح الجديد"، صاحبك مصري جدع.
كلم سامح دايما بالعامية المصرية، زي "يا غالي، يا معلم، من عيوني، أهو".
ردك يكون قصير جدا، سطرين او 3 بالكتير، ودمك خفيف، ومتتكلمش فصحى خالص.
انت دايما بتبعت رد كتابة وبعده فويس بنفس الكلام، اوعى تقول انك بوت كلام بس.
"""

TEXT_MODELS = ["gemini-3.5-flash-lite", "gemini-3.8-flash", "gemini-3-flash-preview"]
IMAGE_MODELS = ["gemini-3-pro-image-preview", "gemini-2.5-flash-image", "gemini-2.0-flash-preview-image-generation"]
IMAGE_WORDS = ["ارسم", "ارسملي", "صورة", "صوره", "تخيل", "اعملي", "رسم", "image", "draw", "picture"]
VOICE = "ar-EG-SalimNeural"

def make_voice_edge(text):
    import edge_tts
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    communicate = edge_tts.Communicate(text, VOICE)
    loop.run_until_complete(communicate.save("voice.mp3"))
    loop.close()

def make_voice_gtts(text):
    from gtts import gTTS
    tts = gTTS(text=text, lang='ar', slow=False)
    tts.save("voice.mp3")

def make_image_pollinations(prompt):
    # ده الموقع المجاني اللي هيرسم لو جوجل رفض
    safe_prompt = urllib.parse.quote(prompt)
    url = f"https://image.pollinations.ai/prompt/{safe_prompt}?width=1024&height=1024&seed=42&nologo=true"
    r = requests.get(url, timeout=60)
    if r.status_code == 200:
        with open("image.png", "wb") as f:
            f.write(r.content)
        return True
    return False

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "اهلا يا سامح! انا اهو معاك، اسألني اي حاجة وهرد عليك كتابة وصوت، ولو قولت ارسملي هبعتلك صورة")

@bot.message_handler(func=lambda m: True)
def ai_reply(message):
    text = message.text

    # لو طلب صورة
    if any(word in text.lower() for word in IMAGE_WORDS):
        bot.send_chat_action(message.chat.id, 'upload_photo')
        bot.reply_to(message, "تمام يا معلم، برسمهالك دلوقتي... 🎨")
        img_done = False

        # 1. يجرب جوجل الاول
        for img_model in IMAGE_MODELS:
            try:
                response = client.models.generate_content(
                    model=img_model,
                    contents=text,
                    config=types.GenerateContentConfig(system_instruction=SYSTEM_PROMPT)
                )
                for part in response.candidates[0].content.parts:
                    if part.inline_data:
                        img = Image.open(io.BytesIO(part.inline_data.data))
                        img.save("image.png")
                        with open("image.png", "rb") as photo:
                            bot.send_photo(message.chat.id, photo, caption="خلصت يا غالي، ايه رايك؟ 😍")
                        img_done = True
                        break
                if img_done:
                    break
            except Exception as e:
                print(f"Image model {img_model} failed: {e}")
                continue

        # 2. لو جوجل فشل، يرسم من الموقع المجاني
        if not img_done:
            try:
                print("Trying Pollinations fallback...")
                if make_image_pollinations(text):
                    with open("image.png", "rb") as photo:
                        bot.send_photo(message.chat.id, photo, caption="خلصت يا غالي، ايه رايك؟ 😍")
                    img_done = True
            except Exception as e:
                print(f"Pollinations failed: {e}")

        if not img_done:
            bot.reply_to(message, "يا غالي معرفتش ارسمها دلوقتي، جرب توصفها بطريقة تانية")
        return

    # لو كلام عادي - كتابة + صوت
    bot.send_chat_action(message.chat.id, 'typing')
    reply_text = ""
    for model_name in TEXT_MODELS:
        try:
            response = client.models.generate_content(
                model=model_name,
                contents=text,
                config=types.GenerateContentConfig(system_instruction=SYSTEM_PROMPT)
            )
            reply_text = response.text
            break
        except Exception:
            continue

    if not reply_text:
        bot.reply_to(message, "انا اهو يا غالي، معاك، جوجل بس كانت زحمة، جرب تاني.")
        return

    bot.reply_to(message, reply_text)

    try:
        bot.send_chat_action(message.chat.id, 'record_voice')
        try:
            make_voice_edge(reply_text[:1000])
        except Exception as e:
            print(f"Edge failed, fallback to gTTS: {e}")
            make_voice_gtts(reply_text[:1000])
        
        with open("voice.mp3", "rb") as voice_file:
            bot.send_voice(message.chat.id, voice_file)
    except Exception as e:
        print(f"Voice error: {e}")

bot.polling(none_stop=True, timeout=60, long_polling_timeout=60)
