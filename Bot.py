pip install telethon pydub
from telethon import TelegramClient, events
from pydub import AudioSegment
import os

# اطلاعات حساب تلگرام
API_ID = "20576032"
API_HASH = "97636bfcf1060ea78960b64fe5bb320c"
PHONE_NUMBER = "+989999003275"

# کانال‌ها
SOURCE_CHANNELS = ["https://t.me/FreeMosic", "https://t.me/PlaylistShiph"]  # کانال‌هایی که می‌خواهید از آنها موسیقی بگیرید
DEST_CHANNEL = "https://t.me/Alirezakz1"  # کانالی که می‌خواهید موسیقی را ارسال کنید

# اتصال به تلگرام
client = TelegramClient("session_name", API_ID, API_HASH)

# تابع برای ساخت دمو (۶۰ ثانیه اول موسیقی)
def create_demo(audio_path):
    sound = AudioSegment.from_file(audio_path)
    demo = sound[:60000]  # استخراج ۶۰ ثانیه اول
    demo_path = "demo_" + audio_path
    demo.export(demo_path, format="mp3")
    return demo_path

# دریافت موسیقی از کانال‌ها
@client.on(events.NewMessage(chats=SOURCE_CHANNELS))
async def music_handler(event):
    if event.audio or event.document:
        file = await event.download_media()
        
        # ساخت دمو
        demo_file = create_demo(file)

        # ارسال به کانال سوم
        await client.send_file(DEST_CHANNEL, file, caption="🎵 موسیقی کامل")
        await client.send_file(DEST_CHANNEL, demo_file, caption="🎶 دمو ۱ دقیقه‌ای")

        # حذف فایل‌های اضافه
        os.remove(file)
        os.remove(demo_file)

# شروع برنامه
with client:
    client.start(phone=PHONE_NUMBER)
    print("ربات در حال اجراست...")
    client.run_until_disconnected()
    