from datetime import datetime as dt
from random import choices
import string

from flask_login import UserMixin
from sqlalchemy import event
from werkzeug.security import check_password_hash, generate_password_hash

from app import db, login
from app.helpers.articles import generate_slug


class User(UserMixin, db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), nullable=False, index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    joined_on = db.Column(db.DateTime, default=dt.utcnow)
    updated_at = db.Column(db.DateTime, default=dt.utcnow, onupdate=dt.utcnow)
    articles = db.relationship(
        "Article", back_populates="user", cascade="all, delete-orphan"
    )
    # about = db.Column(db.String(140), nullable=True)
    password_hash = db.Column(db.String(128))

    def set_password(self, password: str):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password_hash, password)

    def __repr__(self) -> str:
        return f"<User(name={self.username})>"


article_articledata = db.Table(
    "article_articledata",
    db.Column("article_id", db.Integer, db.ForeignKey("articles.id"), primary_key=True),
    db.Column("metadata_id", db.Integer, db.ForeignKey("articledata.id"), primary_key=True),
)


class ArticleData(db.Model):
    __tablename__ = "articledata"

    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.String(64), nullable=False)
    value = db.Column(db.String(256), nullable=False)

    def __repr__(self):
        return f"<ArticleData(key='{self.key}', value='{self.value}')>"


class Article(db.Model):
    __tablename__ = "articles"

    id = db.Column(db.Integer, primary_key=True)
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

    # Define many-to-many relationship with Article
    data = db.relationship(
        "ArticleData",
        secondary=article_articledata,
        lazy="dynamic",
    )

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


@login.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))
