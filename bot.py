import os
import telebot
from openai import OpenAI

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)
client = OpenAI(api_key=OPENAI_API_KEY)


@bot.message_handler(commands=["start"])
def start(message):
    bot.reply_to(
        message,
        "👋 আসসালামু আলাইকুম!\n\nআমি একটি AI Bot। "
        "আপনার প্রশ্ন লিখুন, আমি উত্তর দেওয়ার চেষ্টা করব।"
    )


@bot.message_handler(func=lambda message: True)
def answer(message):
    try:
        response = client.responses.create(
            model="gpt-5-mini",
            input=message.text
        )

        bot.reply_to(message, response.output_text)

    except Exception as e:
        bot.reply_to(message, "দুঃখিত, এই মুহূর্তে উত্তর দিতে পারছি না।")


bot.infinity_polling()
