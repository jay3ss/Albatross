from typing import Optional

from pydantic import BaseModel


class ArticleBase(BaseModel):
    title: str
    author_id: int
    content: str
    summary: Optional[str]
    image_url: Optional[str]


class ArticleCreate(ArticleBase):
    title: str
    author_id: int
    content: str


class ArticleUpdate(ArticleBase):
    id: int


class Article(ArticleBase):
    author_id: int
