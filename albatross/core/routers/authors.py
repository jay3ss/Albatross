from http import HTTPStatus

from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from fastapi.templating import Jinja2Templates

from albatross.core import schemas
from albatross.helpers import database as db
from albatross.settings import config


router = APIRouter(prefix="/authors")

templates = Jinja2Templates(directory=config.templates_dir)


@router.get("/")
async def index(limit: int = None):
    authors = db.get_authors(limit=limit)
    return authors


@router.post("/new", status_code=HTTPStatus.CREATED)
async def create_author(author: schemas.AuthorCreate):
    new_author = db.create_author(author)
    return new_author


@router.get("/{author_id}")
async def read_author(author_id: int):
    author = db.get_author_by_id(author_id=author_id)
    if not author:
        detail = "Author not found"
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=detail)

    return {"author": author}


@router.put("/{author_id}")
async def update_author(author_id: int, author: schemas.AuthorUpdate):
    # NOTE:
    # is using the 'AuthorUpdate' object's 'id' attribute smart?
    # i think that maybe i should use the 'author_id' to find the
    # 'Author' and then use the 'AuthorUpdate' object for the rest
    # of the data...
    updated_author = db.update_author(author=author)
    if not updated_author:
        detail = "Author not found"
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=detail)

    return {"author": updated_author}


@router.delete("/{author_id}")
async def delete_author(author_id: int):
    was_deleted = db.delete_author(author_id=author_id)
    if not was_deleted:
        detail = "Author not found"
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=detail)

    return {"deleted": was_deleted}
