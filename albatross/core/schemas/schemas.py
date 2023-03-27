from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class ArticleBase(BaseModel):
    id: int
    title: str
    author: str
    content: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    summary: Optional[str]
    image_url: Optional[str]


class ArticleCreate(ArticleBase):
    author_id: int


class ArticleUpdate(ArticleBase):
    pass


class Article(ArticleBase):
    id: int
    created_at: datetime
    updated_at: datetime
    author_id: int

    class Config:
        orm_mode = True


class Author(BaseModel):
    id: int = Field(..., title="ID", description="The ID of the author")
    name: str = Field(..., title="Name", description="The name of the author")
    created_at: datetime = Field(
        ...,
        title="Created at",
        description="The date and time when the author was created",
    )
    updated_at: datetime = Field(
        ...,
        title="Updated at",
        description="The date and time when the author was last updated",
    )

    class Config:
        orm_mode = True
