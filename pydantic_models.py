from datetime import datetime
from pydantic import BaseModel, Field


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


class Post(BaseModel):
    id: int
    title: str
    author: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    markdown_path: str
    summary: str
    image_url: str
