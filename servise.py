from typing import List, Optional

from models import User, Song, session

from sqlalchemy.orm import joinedload


def user_exists(chat_id: int) -> bool:
    """Существует ли пользователь."""

    with session() as sess:
        user = sess.query(User).where(User.chat_id == chat_id).first()
        if not user:
            return False
    return True


def get_all_songs() -> List[Song]:
    """Достаём из базы все песни."""

    with session() as sess:
        songs = sess.query(Song).options(
            joinedload(Song.user)
        ).all()
        return songs


def get_user_songs(user_id) -> List[Song]:
    """Достаём из базы песни пользователя."""

    with session() as sess:
        songs = sess.query(Song).options(
            joinedload(Song.user)
        ).where(Song.user_id == user_id).all()
        return songs


def get_user_by_chat_id(chat_id) -> Optional[User]:
    """Достаём Пользователя по chat_id."""

    with session() as sess:
        user = sess.query(User).where(User.chat_id == chat_id).first()
        return user


def get_message_from_songs(songs: List[Song]) -> str:
    """Создать текстовое сообщение из Песен."""

    text = ''
    for song in songs:
        text += str(song)
        text += '\n'
    return text


def save_song(song: Song):
    """Сохранить песню в базе."""

    with session() as sess:
        sess.add(song)
        sess.commit()


def save_user(user: User):
    """Сохранить пользователя."""

    with session() as sess:
        sess.add(user)
        sess.commit()


def delete_song(song: Song):
    """Удалить песню."""

    with session() as sess:
        sess.delete(song)
        sess.commit()


def get_song_by_id(song_id: int):
    """Получить песню по id."""

    with session() as sess:
        song = sess.query(Song).options(
            joinedload(Song.user)
        ).where(Song.id == song_id).first()
        return song
