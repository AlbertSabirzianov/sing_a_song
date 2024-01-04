"""
  Бот для вокалистов, позаоляет добавлять и удалять
  песни, которые собираются исполнять на концерте.
"""

import os

import telebot
from dotenv import load_dotenv

from models import Base, engine, User, Song
import servise

load_dotenv()

TOKEN = os.getenv('SINGERS_BOT_TOKEN')

bot = telebot.TeleBot(token=TOKEN)


def registration(message):
    """Регистрация Пользователя."""

    user = User(
        chat_id=message.chat.id,
        username=message.chat.username
    )
    user.name = message.text
    servise.save_user(user)
    murkup = telebot.types.ReplyKeyboardMarkup()
    create_song_btn = telebot.types.KeyboardButton('Добавить песню')
    my_songs_btn = telebot.types.KeyboardButton('Мои песни')
    delete_song_btn = telebot.types.KeyboardButton('Удалить песню')
    murkup.row(my_songs_btn)
    murkup.row(create_song_btn, delete_song_btn)
    bot.send_message(
        message.chat.id,
        'Бот работает! Теперь вы можете добавлять песни,'
        ' которые собираетесь исполнять!',
        reply_markup=murkup
    )


@bot.message_handler(commands=['start'])
def start(message):
    """Старт Бота."""

    if not servise.user_exists(message.chat.id):
        bot.send_message(
            message.chat.id,
            'Для использования бота напишете своё имя, пожалуйста:'
        )
        bot.register_next_step_handler(message, registration)
    else:
        murkup = telebot.types.ReplyKeyboardMarkup()
        create_song_btn = telebot.types.KeyboardButton('Добавить песню')
        my_songs_btn = telebot.types.KeyboardButton('Мои песни')
        delete_song_btn = telebot.types.KeyboardButton('Удалить песню')
        murkup.row(my_songs_btn)
        murkup.row(create_song_btn, delete_song_btn)
        bot.send_message(
            message.chat.id,
            'Бот работает! Теперь вы можете добавлять песни,'
            ' которые собираетесь исполнять!',
            reply_markup=murkup
        )


@bot.message_handler()
def user_button_input(message):
    """Обрабатываем нажатие на кнопки от пользователя."""

    # if message.text == "Все песни":
    #     songs = servise.get_all_songs()
    #     if not songs:
    #         bot.send_message(message.chat.id, 'Песни ещё не добавленны')
    #     else:
    #         text = servise.get_message_from_songs(songs)
    #         bot.send_message(message.chat.id, text, parse_mode='Markdown')

    if message.text == 'Мои песни':
        user = servise.get_user_by_chat_id(message.chat.id)
        songs = servise.get_user_songs(user.id)
        if not songs:
            bot.send_message(message.chat.id, 'Вы ещё не добавили песен')
        else:
            text = servise.get_message_from_songs(songs)
            bot.send_message(message.chat.id, text, parse_mode='Markdown')

    if message.text == 'Добавить песню':
        user = servise.get_user_by_chat_id(message.chat.id)
        song = Song(user_id=user.id)
        bot.send_message(message.chat.id, 'Введите название песни:')
        bot.register_next_step_handler(message, add_name_to_song, song=song)

    if message.text == 'Удалить песню':
        bot.send_message(message.chat.id, "Ведите номер id песни, которую хотите удалить")
        bot.register_next_step_handler(message, get_song_id_from_user_and_delete)


def get_song_id_from_user_and_delete(message):
    """Получаем id Песни от пользователя и удаляем её."""

    user = servise.get_user_by_chat_id(message.chat.id)
    song_id = message.text
    try:
        song_id = int(song_id)
    except Exception:
        bot.send_message(message.chat.id, 'id строго числовое значение!')
        return

    song = servise.get_song_by_id(song_id)
    if not song:
        bot.send_message(message.chat.id, 'Такой песни не существует!')
    elif song.user_id != user.id:
        bot.send_message(message.chat.id, 'Удалить можно только свой песню')
    else:
        servise.delete_song(song)
        bot.send_message(message.chat.id, 'Песня успешно удалена!')


def add_name_to_song(message, song: Song):
    """Добавляем название песне."""

    song.name = message.text
    bot.send_message(message.chat.id, 'Введите ссылку на запись:')
    bot.register_next_step_handler(message, add_link_to_song, song=song)


def add_link_to_song(message, song: Song):
    """Добавляем ссылку песне."""

    song.link = message.text
    bot.send_message(message.chat.id, 'Введите коментарий (Тональность, оссобенности формы):')
    bot.register_next_step_handler(message, add_comment_to_song, song=song)


def add_comment_to_song(message, song: Song):
    """Добавляем коментарий песне и сохраняем в базе."""

    song.comment = message.text
    servise.save_song(song)
    bot.send_message(message.chat.id, 'Песня успешно добавленна!')


if __name__ == '__main__':
    Base.metadata.create_all(engine)
    bot.infinity_polling()
