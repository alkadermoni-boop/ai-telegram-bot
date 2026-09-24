import os
import threading
import telebot
from openai import OpenAI
from flask import Flask

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)
client = OpenAI(api_key=OPENAI_API_KEY)

app = Flask(__name__)


@app.route("/")
def home():
    return "AI Telegram Bot is running!"


@bot.message_handler(commands=["start"])
def start(message):
    bot.reply_to(
        message,
        "👋 আসসালামু আলাইকুম!\n\n"
        "আমি একটি AI Bot। আপনার প্রশ্ন লিখুন।"
    )


@bot.message_handler(func=lambda message: True)
def answer(message):
    try:
        response = client.responses.create(
            model="gpt-5.6-luna",
            input=message.text
        )

        bot.reply_to(message, response.output_text)

    except Exception:
        bot.reply_to(
            message,
            "দুঃখিত, এই মুহূর্তে উত্তর দিতে পারছি না।"
        )


def run_web():
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)


threading.Thread(target=run_web, daemon=True).start()

bot.infinity_polling(skip_pending=True)
