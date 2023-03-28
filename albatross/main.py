from fastapi import FastAPI, HTTPException, Request, Response
from fastapi.responses import RedirectResponse

from albatross.core.routers import authors

app = FastAPI()
app.include_router(authors.router)


@app.post("/articles/")
async def create_post(request: Request, response: Response):
    # create the article here

    response = RedirectResponse(url="/articles/")
    return response
