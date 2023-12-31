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
    phone_number: Mapped[str]
    chat_id: Mapped[int]

    songs: Mapped[List['Song']] = relationship(
        back_populates='user', cascade='all, delete-orphan'
    )


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
        text += f'_id {self.id}_ \n'
        text += f'*{self.name}* \n'
        text += f'_{self.link}_ \n'
        text += f'_Исполнитель {self.user.name} {self.user.phone_number}_\n'
        text += f'_Коментарий {self.comment}_\n'
        return text
