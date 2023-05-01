import string
from datetime import datetime as dt
from random import choices
from time import time

import jwt
from flask import current_app
from flask_login import UserMixin
from sqlalchemy import event
from sqlalchemy.orm import Mapped, mapped_column
from werkzeug.security import check_password_hash, generate_password_hash

from app import db, login
from app.helpers.articles import generate_slug


class User(UserMixin, db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), nullable=False, index=True, unique=True)
    username_lower = db.Column(db.String(128), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), index=True, unique=True)
    joined_on = db.Column(db.DateTime, default=dt.utcnow)
    updated_at = db.Column(db.DateTime, default=dt.utcnow, onupdate=dt.utcnow)
    articles = db.relationship(
        "Article", back_populates="user", cascade="all, delete-orphan"
    )
    about = db.Column(db.String(280), nullable=True)
    password_hash = db.Column(db.String(128))

    def set_password(self, password: str):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password_hash, password)

    def get_reset_password_token(self, expires_in=600):
        return jwt.encode(
            payload={"reset_password": self.id, "exp": time() + expires_in},
            key=current_app.config["SECRET_KEY"],
            algorithm="HS256"
        )

    @staticmethod
    def verify_reset_password_token(token):
        try:
            user_id = jwt.decode(
                jwt=token,
                key=current_app.config["SECRET_KEY"],
                algorithms=["HS256"]
            )["reset_password"]
        except:
            return
        return db.session.get(User, user_id)

    @property
    def num_drafts(self) -> int:
        """
        Returns the number of articles that are marked as a draft.

        Returns:
            int: the number of articles that are marked as a draft.
        """
        return len([a for a in self.articles if a.is_draft])

    @property
    def num_published(self) -> int:
        """
        Returns the number of articles that are marked as a draft.

        Returns:
            int: the number of articles that are marked as a draft.
        """
        return len([a for a in self.articles if not a.is_draft])

    @staticmethod
    def is_username_taken(username: str) -> bool:
        """
        Checks if the given username is taken

        Args:
            username (str): The username to check

        Returns:
            bool: True if the username is taken, False otherwise
        """
        user = User.query.filter_by(username_lower=username.lower()).first()
        return user is not None

    @staticmethod
    def is_email_taken(email: str) -> bool:
        """
        Checks if the given email is taken

        Args:
            email (str): The email to check

        Returns:
            bool: True if the email is taken, False otherwise
        """
        user = User.query.filter_by(email=email.lower()).first()
        return user is not None

    def __repr__(self) -> str:
        return f"<User(name={self.username})>"


article_data_association_table = db.Table(
    "article_data_association_table",
    db.Column("articledata_id", db.ForeignKey("articles.id"), primary_key=True),
    db.Column("article_id", db.ForeignKey("articledata.id"), primary_key=True),
)


class ArticleData(db.Model):
    __tablename__ = "articledata"

    id: Mapped[int] = mapped_column(primary_key=True)
    key = db.Column(db.String(64), nullable=False)
    value = db.Column(db.String(256), nullable=False)
    article_id = db.Column(db.Integer, db.ForeignKey("articles.id"))
    articles: Mapped[list["Article"]] = db.relationship(
        "Article", secondary=article_data_association_table, back_populates="data"
    )

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "key": self.key,
            "value": self.value,
            "article_ids": [article.id for article in self.articles]
        }

    def __repr__(self):
        return f"<ArticleData(key='{self.key}', value='{self.value}')>"


class Article(db.Model):
    __tablename__ = "articles"

    id: Mapped[int] = mapped_column(primary_key=True)
    title = db.Column(db.String, nullable=False)
    summary = db.Column(db.Text)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=dt.utcnow)
    updated_at = db.Column(db.DateTime, default=dt.utcnow, onupdate=dt.utcnow)
    image_url = db.Column(db.String)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=True)
    user = db.relationship("User")
    slug = db.Column(db.String, unique=True, name="uq_article_slug", index=True)
    is_draft = db.Column(db.Boolean, default=True, nullable=False)

    # Define many-to-many relationship with ArticleData
    data: Mapped[list[ArticleData]] = db.relationship(
        "ArticleData", secondary=article_data_association_table, back_populates="articles"
    )

    def filter_data_by_key(self, key: str) -> list["Article"]:
        """
        Get the ArticleData object associated with the given key for this Article.

        Args:
            key (str): The key to search for in the Article's data.

        Returns:
            ArticleData or None: The ArticleData object if found, else None.
        """
        article_data = list(filter(lambda e: e.key==key, self.data))
        return article_data

    @staticmethod
    def generate_slug(title: str) -> str:
        """
        Generate slug from title.

        Args:
            title (str): The title to generate slug from.

        Returns:
            str: The generated slug.
        """
        return generate_slug(title)

    def __repr__(self) -> str:
        if not self.user:
            return f"<Article(title='{self.title}')>"
        return f"<Article(title='{self.title}', user='{self.user.username}')>"


# Define an event listener to generate slug before insert
@event.listens_for(Article, "before_insert")
def generate_slug_before_insert(mapper, connection, target):
    slug = Article.generate_slug(target.title)
    while Article.query.filter_by(slug=slug).first() is not None:
        # Slug already exists, append a random letter or digit to make it unique
        random_char = choices(string.ascii_letters + string.digits, k=1)[
            0
        ]  # pragma: no cover
        slug = f"{slug}{random_char}"  # pragma: no cover
    target.slug = slug


# Define an event listener to generate slug before update
# @event.listens_for(Article, "before_update")
# def generate_slug_before_update(mapper, connection, target):
#     slug = Article.generate_slug(target.title)
#     while Article.query.filter_by(slug=slug).filter(Article.id != target.id).first() is not None:
#         # Slug already exists, append a random letter or digit to make it unique
#         random_char = choices(string.ascii_letters + string.digits, k=1)[0] # pragma: no cover
#         slug = f"{slug}{random_char}" # pragma: no cover
#     target.slug = slug


# Define an event listener to set the lowercase version of the user's email
@event.listens_for(User, "before_insert")
def generate_slug_before_insert(mapper, connection, target):
    target.email = target.email.lower()


# Define an event listener to set the lowercase version of the user's email
@event.listens_for(User, "before_update")
def generate_slug_before_update(mapper, connection, target):
    target.email = target.email.lower()


# Define an event listener to set the lowercase version of the user's username
@event.listens_for(User, "before_insert")
def generate_slug_before_insert(mapper, connection, target):
    target.username_lower = target.username.lower()


# Define an event listener to set the lowercase version of the user's username
@event.listens_for(User, "before_update")
def generate_slug_before_update(mapper, connection, target):
    target.username_lower = target.username.lower()


# Define an event listener to set the updated datetime
@event.listens_for(User, "before_update")
def generate_slug_before_update(mapper, connection, target):
    target.updated_at = dt.utcnow()


@login.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))
