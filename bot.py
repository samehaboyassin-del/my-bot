import os
import io
import asyncio
import re
import requests
import urllib.parse
import random
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
اوعى تكتب [فويس نوت] او (فويس) او اي رمز فويس في الكتابة، انت بتبعت الكتابة بس والفويس بيتبعت لوحده.
لو قالك "روحت فين" او "نبدأ من الاول" رد عليه "انا اهو يا غالي، معاك، نبدأ من الاول".
"""

TEXT_MODELS = ["gemini-3.5-flash-lite", "gemini-3.8-flash", "gemini-3-flash-preview"]
IMAGE_MODELS = ["gemini-3-pro-image-preview", "gemini-2.5-flash-image", "gemini-2.0-flash-preview-image-generation"]
IMAGE_WORDS = ["ارسم", "ارسملي", "صورة", "صوره", "تخيل", "اعملي", "رسم", "image", "draw", "picture"]
VOICE = "ar-EG-SalimNeural"

def clean_reply(text):
    # بيشيل اي هبل زي [فويس نوت] اللي البوت بيألفه
    text = text.replace("[فويس نوت]", "").replace("[فويس نوت]:", "").replace("🎙️", "").replace("🎤", "")
    text = re.sub(r"\(.*فويس.*\)", "", text)
    text = re.sub(r"\[.*?\]", "", text)
    return text.strip()

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

def translate_to_english(arabic_prompt):
    # بيكتب وصف تفصيلي جدا بالانجليزي عشان موقع الصور يفهمه صح
    try:
        for model_name in TEXT_MODELS:
            try:
                resp = client.models.generate_content(
                    model=model_name,
                    contents=f"""
                    You are an expert image prompt writer.
                    User wants in Arabic: {arabic_prompt}
                    Write ONE detailed English prompt for an AI image generator.
                    Rules:
                    - Be very specific: colors, animals, place, action
                    - If user says cat and dog, write: "A cute orange cat and a small brown dog playing together in a garden, no people, no humans, no women"
                    - If user says cat only, write: "A cute fluffy cat, no people"
                    - Never include people unless user asked for people.
                    - Add at end: "photorealistic, high quality, cute, detailed"
                    - Output ONLY the English prompt, nothing else.
                    """
                )
                if resp.text:
                    return resp.text.strip().replace("\n", " ")
            except:
                continue
    except:
        pass
    return arabic_prompt + ", no people, photorealistic"

def make_image_pollinations(prompt):
    english_prompt = translate_to_english(prompt)
    print(f"Original: {prompt} -> English: {english_prompt}")
    safe_prompt = urllib.parse.quote(english_prompt)
    seed = random.randint(1, 999999)
    url = f"https://image.pollinations.ai/prompt/{safe_prompt}?width=1024&height=1024&seed={seed}&model=flux&nologo=true&enhance=true&safe=true"
    r = requests.get(url, timeout=90)
    if r.status_code == 200 and len(r.content) > 10000:
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
                if make_image_pollinations(text):
                    with open("image.png", "rb") as photo:
                        bot.send_photo(message.chat.id, photo, caption="خلصت يا غالي، ايه رايك؟ 😍 لو مش عجباك قولي ارسم غيرها")
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

    reply_text = clean_reply(reply_text)
    bot.reply_to(message, reply_text)

    # الصوت - يجرب صوت الراجل المصري الاول، لو فشل يجرب الصوت القديم
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
