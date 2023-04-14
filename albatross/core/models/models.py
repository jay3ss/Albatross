from datetime import datetime
from albatross import db

# Base = declarative_base()


# class Author(Base):
class Author(db.Model):
    __tablename__ = "authors"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    articles = db.relationship(
        "Article", back_populates="author", cascade="all, delete-orphan"
        )

    def __repr__(self) -> str:
        return f"<Author(name={self.name})>"


# class Article(Base):
class Article(db.Model):
    __tablename__ = "articles"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    summary = db.Column(db.Text)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    image_url = db.Column(db.String)
    author_id = db.Column(db.Integer, db.ForeignKey("authors.id"), nullable=True)
    author = db.relationship("Author")

    def __repr__(self) -> str:
        return f"<Article(title='{self.title}', author='{self.author.name}')>"
