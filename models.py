import os
from typing import Optional, List

from dotenv import load_dotenv

from sqlalchemy import create_engine, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship, sessionmaker

load_dotenv()

engine = create_engine(os.getenv('DATABASE_PATH'), echo=True)
session = sessionmaker(engine)


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = 'user'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    username: Mapped[Optional[str]]
    chat_id: Mapped[int]

    songs: Mapped[List['Song']] = relationship(
        back_populates='user', cascade='all, delete-orphan'
    )

    def __str__(self):
        
        text = ''
        text += f'{self.name} \n'
        text += f'@{self.username} \n'
        text += 'Песни: '
        for song in self.songs:
            text += f'{song.name}, '
        text += '\n\n'
        return text


class Song(Base):
    __tablename__ = 'song'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    link: Mapped[str]
    comment: Mapped[Optional[str]]

    # fk
    user_id: Mapped[int] = mapped_column(ForeignKey('user.id'))

    user: Mapped['User'] = relationship(back_populates='songs')

    def __str__(self):
        text = ''
        text += f'id {self.id} \n'
        
        text += f'{self.name} \n'
        text += f'{self.link} \n'
        # text += f'__Исполнитель__ \n _{self.user.name}_ \n' \
        #         f'__Контакт__ \n _{self.user.username}_\n'
        text += f'{self.comment}\n'

        return text
