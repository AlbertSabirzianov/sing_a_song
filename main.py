import os

import telebot
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv('TOKEN')

bot = telebot.TeleBot(token=TOKEN)


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, 'Hi')


if __name__ == '__main__':
    bot.infinity_polling()
