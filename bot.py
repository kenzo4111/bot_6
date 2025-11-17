from flask import Flask
import threading
import telebot

app = Flask(__name__)

@app.route("/", methods=["GET"])
def home():
    return "salom bot ishlayapti", 200

# ======================================
# BOT
BOT_TOKEN = "7359713313:AAGbK1Bj_k1dRt259fRkUM0fn4g_Gau79_8"

bot = telebot.TeleBot(BOT_TOKEN)
# ======================================
# Botni kodlari

import telebot
import instaloader
import os

BOT_TOKEN = "7359713313:AAGbK1Bj_k1dRt259fRkUM0fn4g_Gau79_8"

bot = telebot.TeleBot(BOT_TOKEN)

loader = instaloader.Instaloader(
    download_comments=False,
    download_geotags=False,
    download_pictures=False,
    download_video_thumbnails=False,
    save_metadata=False
)

# start bosilganda
@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "salom! bot ishlavotdi!")
    
@bot.message_handler(func=lambda message: True)
def echo_all(message):
    # habardagi urlni olish
    url = message.text

    # url togriligini tekshrsh
    try:
        shortcode = url.split("/")[-2]
    except IndexError:
        bot.reply_to(message, "link notogri")
        return

    try: 
        loader_message = bot.send_message(message.chat.id, "video yuklanyapti...")

        # videoni yuklash
        post = instaloader.Post.from_shortcode(loader.context, shortcode)
        loader.download_post(post, target=shortcode)

        # yuklangan vidoeni nomini aniqlash
        video_file = None
        for file in os.listdir(shortcode):
            if file.endswith(".mp4"):
                video_file = os.path.join(shortcode, file)
                break

        # osha videoni yuborish
        if video_file:
            with open(video_file, "rb") as video:
                bot.send_video(message.chat.id, video)
                bot.delete_message(message.chat.id, loader_message.message_id)
            
            # va videoni ochirib tashlash
            for f in os.listdir(shortcode):
                os.remove(os.path.join(shortcode, f))
            os.rmdir(shortcode)
        else: 
            # agar video topilmasa
            bot.delete_message(message.chat.id, loader_message.message_id)
            bot.reply_to(message, "video topilmadi")

    except Exception:
        # xatolik yuzb bersa
        bot.delete_message(message.chat.id, loader_message.message_id)
        bot.reply_to(message, "video yuklashda xatolik yuz berdi")

bot.infinity_polling()





@bot.message_handler(commands=["start"])
def start(msg):
    bot.reply_to(msg, "Salom, bot ishlavotd!")

# ======================================
#  Botni va Serverni ishga tushrsh

def run_bot():
    bot.polling(non_stop=True)

if __name__ == "__main__":
    threading.Thread(target=run_bot).start()
    app.run(host="0.0.0.0", port=5000, debug=True)
