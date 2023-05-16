import json
import string
from datetime import datetime as dt
from pathlib import Path
from random import choices
from time import time
from typing import Any

import jwt
import mistune
from flask import current_app
from flask_login import UserMixin
from pelican import read_settings
from sqlalchemy import event
from sqlalchemy.orm import Mapped, mapped_column
from werkzeug.security import check_password_hash, generate_password_hash

from app import db, login
from app.helpers.articles import HighlightRenderer, generate_slug
from app.helpers.settings import _default_settings_string, _write_dict_to_file


class User(UserMixin, db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), nullable=False, index=True, unique=True)
    username_lower = db.Column(db.String(128), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), index=True, unique=True)
    joined_on = db.Column(db.DateTime, default=dt.utcnow)
    updated_at = db.Column(db.DateTime, onupdate=dt.utcnow)
    articles = db.relationship(
        "Article", back_populates="user", cascade="all, delete-orphan"
    )
    about = db.Column(db.String(280), nullable=True)
    password_hash = db.Column(db.String(128))
    settings = db.relationship("UserSettings", uselist=False, backref="user")

    def set_password(self, password: str):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password_hash, password)

    def get_reset_password_token(self, expires_in=600):
        return jwt.encode(
            payload={"reset_password": self.id, "exp": time() + expires_in},
            key=current_app.config["SECRET_KEY"],
            algorithm="HS256",
        )

    @staticmethod
    def verify_reset_password_token(token):
        try:
            user_id = jwt.decode(
                jwt=token, key=current_app.config["SECRET_KEY"], algorithms=["HS256"]
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
    # TODO: make it so that they key-value tuple is unique
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
            "article_ids": [article.id for article in self.articles],
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
    # updated_at = db.Column(db.DateTime, default=dt.utcnow, onupdate=dt.utcnow)
    updated_at = db.Column(db.DateTime, nullable=True, onupdate=dt.utcnow)
    image_url = db.Column(db.String)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=True)
    user = db.relationship("User")
    slug = db.Column(db.String, unique=True, name="uq_article_slug", index=True)
    is_draft = db.Column(db.Boolean, default=True, nullable=False)

    # Define many-to-many relationship with ArticleData
    data: Mapped[list[ArticleData]] = db.relationship(
        "ArticleData",
        secondary=article_data_association_table,
        back_populates="articles",
    )

    def filter_data_by_key(self, key: str) -> list["Article"]:
        """
        Get the ArticleData object associated with the given key for this Article.

        Args:
            key (str): The key to search for in the Article's data.

        Returns:
            ArticleData or None: The ArticleData object if found, else None.
        """
        article_data = list(filter(lambda e: e.key == key, self.data))
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

    @property
    def content_html(self) -> str:
        plugins = [
            "abbr",
            "def_list",
            "footnotes",
            # "insert",
            # "mark",
            # "math",
            # "spoiler",
            "strikethrough",
            # "subscript",
            # "superscript",
            "table",
            "task_lists",
        ]
        md = mistune.create_markdown(renderer=HighlightRenderer(), plugins=plugins)
        return md(self.content)

    def __repr__(self) -> str:
        if not self.user:
            return f"<Article(title='{self.title}')>"
        return f"<Article(title='{self.title}', user='{self.user.username}')>"


class UserSettings(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), unique=True)
    settings = db.Column(db.LargeBinary, default=_default_settings_string, nullable=True)

    def to_dict(self) -> dict:
        return json.loads(self.settings)

    def update(self, new_settings: dict | Path | str) -> "UserSettings":
        """
        Updates the settings with contents of the new settings

        Args:
            new_settings (dict | Path | str): Either a dict of the settings
            to update the current settings with or a Path (str too) to the file
            of new settings.

        Returns:
            Settings: the updated Settings instance.
        """
        if isinstance(new_settings, dict):
            settings_dict = self.to_dict()
            settings_dict.update(new_settings)
            encoded_settings = json.dumps(settings_dict)
            self.settings = encoded_settings
        else:
            with open(new_settings, "r") as f:
                self.settings = f.read().encode("utf-8")

        return self

    def write(self, fname: Path | str = "user_settings.json") -> Path:
        """
        Writes the settings to the given file

        Args:
            fname (Path | str, optional): Path or filename to write
            the settings to. Defaults to None. If None, the file will be in the
            working directory in with the filename 'user_settings.json'

        Returns:
            Path: path to the file
        """
        return _write_dict_to_file(fname=fname, contents=self.to_dict())

    @staticmethod
    def create_settings_file(fname: Path | str | None = None) -> Path:
        """
        Creates the settings file with the given filename.

        Args:
            fname (Path | str | None, optional): Path or filename to write the
            settings to. Defaults to None. If None, the file will be in the
            working directory in with the filename 'user_settings.json'.
            Defaults to None.

        Returns:
            Path: Path to the file
        """
        return _write_dict_to_file(fname=fname, contents=read_settings())

    @staticmethod
    def _get_pelican_settings(
        path: Path | str | None = None, override: dict | None = None
    ) -> dict:
        """
        Retrieves the app's settings (including user settings)

        Args:
            path (Path | str | None, optional): Path to the settings file.
                Defaults to None.
            override (dict | None, optional): The settings to override and their
            values. Defaults to None.

        Returns:
            dict: Pelican's settings
        """
        return read_settings(path=path, override=override)

    def __eq__(self, other_settings: dict) -> bool:
        return self.to_dict() == other_settings

    def get(self, key, default: Any = None) -> Any:
        """
        Gets a top-level key-value pair from the settings

        Args:
            key (_type_): The top-level key to get
            default (Any, optional): Default value if key doesn't exist.
            Defaults to None.

        Returns:
            Any: The value at the key, or default if the key doesn't exist
        """
        return self.to_dict().get(key, default)

    def set(self, key, value) -> None:
        settings_dict = self.to_dict()
        settings_dict[key] = value
        self.settings = json.dumps(settings_dict).encode("utf-8")

    def __str__(self) -> str:
        return json.dumps(self.to_dict(), indent=4)





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
def lower_email_before_insert(mapper, connection, target):
    target.email = target.email.lower()


# Define an event listener to set the lowercase version of the user's email
@event.listens_for(User, "before_update")
def lower_email_before_update(mapper, connection, target):
    target.email = target.email.lower()


# Define an event listener to set the lowercase version of the user's username
@event.listens_for(User, "before_insert")
def lower_username_before_insert(mapper, connection, target):
    target.username_lower = target.username.lower()


# Define an event listener to set the lowercase version of the user's username
@event.listens_for(User, "before_update")
def lower_username_before_update(mapper, connection, target):
    target.username_lower = target.username.lower()


@login.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))
