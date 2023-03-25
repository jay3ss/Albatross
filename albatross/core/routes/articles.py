from fastapi import APIRouter

from albatross.helpers import database as db


router = APIRouter(prefix="articles")
engine = db.get_engine()


@router.get("/")
async def index():
    articles = db.get_articles(limit=10)
    return {"articles": articles}


@router.get("/{id}")
async def read_article(id: int):
    return {"article": f"article {id}"}


@router.get("/new")
async def new_article():
    return {"article": ["new article"]}


@router.get("{id}/edit/")
async def edit_article(id: int):
    return {"article": [id]}


@router.get("{id}/delete/")
async def delete_article(id: int):
    return {"article": "deleted"}
