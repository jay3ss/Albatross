from fastapi import FastAPI, HTTPException, Request, Response
from fastapi.responses import RedirectResponse


app = FastAPI()


@app.post("/articles/")
async def create_post(request: Request, response: Response):
    # create the article here

    response = RedirectResponse(url="/articles/")
    return response
