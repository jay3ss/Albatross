from datetime import datetime

from fastapi_users.db import SQLAlchemyUserDatabase, SQLAlchemyBaseUserTable
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

from albatross.helpers.database import get_session


Base = declarative_base()


class User(Base, SQLAlchemyBaseUserTable):
    pass


class Author(Base):
    __tablename__ = "authors"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    posts = relationship("Post", back_populates="author")

    def __repr__(self) -> str:
        return f"<Author(name={self.name})>"


class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    summary = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    markdown_path = Column(String, nullable=False)
    image_url = Column(String)
    author_id = Column(Integer, ForeignKey("authors.id"), nullable=False)
    author = relationship("Author")

    def __repr__(self) -> str:
        return f"<Post(title='{self.title}', author='{self.author.name}')>"


user_db = SQLAlchemyUserDatabase(get_session, User)
