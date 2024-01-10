"""
  Бот для участников трио, позволяет смотреть все
  композиции и всех исполнителей.
"""

import os

import telebot
from dotenv import load_dotenv

import servise

load_dotenv()

TOKEN = os.getenv('TRIO_BOT_TOKEN')

bot = telebot.TeleBot(token=TOKEN)


@bot.message_handler(commands=['start'])
def start(message):
    """Старт бота."""

    markup = telebot.types.ReplyKeyboardMarkup()
    all_songs_btn = telebot.types.KeyboardButton('Все песни')
    all_users_btn = telebot.types.KeyboardButton('Все исполнители')
    markup.row(all_songs_btn, all_users_btn)

    bot.send_message(
        message.chat.id,
        'Бот работает! Теперь вы можете просматривать все песни,'
        ' а  так же всех исполнителей!',
        reply_markup=markup
    )


@bot.message_handler()
def user_button_input(message):
    """Обрабатываем нажатие на кнопки от пользователя."""

    if message.text == "Все песни":
        songs = servise.get_all_songs()
        if not songs:
            bot.send_message(message.chat.id, 'Песни ещё не добавленны')
        else:
            text = servise.get_message_from_songs_for_trio(songs)
            bot.send_message(message.chat.id, text)
    if message.text == 'Все исполнители':
        users = servise.get_all_users()
        if not users:
            bot.send_message(message.chat.id, 'Исполнителей ещё нет')
        else:
            text = servise.get_message_from_songs(users)
            bot.send_message(message.chat.id, text)


if __name__ == '__main__':
    bot.infinity_polling()
