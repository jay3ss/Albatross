from fastapi import FastAPI, HTTPException, Request, Response
from fastapi.responses import RedirectResponse


app = FastAPI()


@app.post("/posts/")
async def create_post(request: Request, response: Response):
    # create the post here

    response = RedirectResponse(url="/posts/")
    return response
