from http import HTTPStatus

from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from albatross.core import schemas
from albatross.helpers import database as db
from albatross.helpers import templates as th
from albatross.settings import config


router = APIRouter(prefix="/authors")

templates = Jinja2Templates(directory=config.templates_dir)
templates.env.filters["datetime_format"] = th.datetime_format


@router.get("/", name="read_authors")
async def index(request: Request, limit: int = None):
    authors = db.get_authors(limit=limit)
    return templates.TemplateResponse(
        name="authors/index.html",
        context={"request": request, "authors": authors}
    )


@router.post("/new", status_code=HTTPStatus.CREATED, name="create_author")
async def create_author(author: schemas.AuthorCreate):
    new_author = db.create_author(author)
    return new_author


@router.get("/{author_id}", name="read_author", response_class=HTMLResponse)
async def read_author(request: Request, author_id: int):
    author = db.get_author_by_id(author_id=author_id)
    if not author:
        detail = "Author not found"
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=detail)

    return templates.TemplateResponse(
        name="authors/show.html",
        context={"request": request, "author": author}
    )


@router.put("/{author_id}", name="update_author")
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


@router.delete("/{author_id}", name="delete_author")
async def delete_author(author_id: int):
    was_deleted = db.delete_author(author_id=author_id)
    if not was_deleted:
        detail = "Author not found"
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=detail)

    return {"deleted": was_deleted}
