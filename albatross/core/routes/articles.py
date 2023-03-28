from fastapi import APIRouter

from albatross.helpers import database as db


router = APIRouter(prefix="articles")


@router.get("/")
async def index():
    articles = db.get_articles(limit=10)
    return {"articles": articles}


@router.get("/{id}")
async def read_article(id: int):
    article = db.get_article(id)
    return {"article": article}


@router.get("/new")
async def new_article():
    return {"article": ["new article"]}


@router.get("{id}/edit/")
async def edit_article(id: int):
    article = db.get_article(id)
    return {"article": article}


@router.get("{id}/delete/")
async def delete_article(id: int):
    article = db.get_article(id)
    return {"article": "deleted"}
