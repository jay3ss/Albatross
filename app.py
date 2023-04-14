from app import create_app, db, models


app = create_app()


@app.make_shell_context
def make_shell_context():
    return {"db": db, "models": models}
