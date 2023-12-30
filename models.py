from typing import Optional, List

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class Singer(Base):
    __tablename__ = 'user'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    phone_number: Mapped[str]

    songs: Mapped[List['Song']] = relationship(
        back_populates='singer', cascade='all, delete-orphan'
    )


class Song(Base):
    __tablename__ = 'song'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    link: Mapped[str]
    comment: Mapped[Optional[str]]

    singer: Mapped['Singer'] = relationship(back_populates='songs')


if __name__ == '__main__':
    engine = create_engine("sqlite:///sqlite.db", echo=True)
    Base.metadata.create_all(engine)
