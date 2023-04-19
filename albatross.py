from albatross import create_app, db, models, schemas


app = create_app()


@app.make_shell_context
def make_shell_context():
    return {"db": db, "models": models, "schemas": schemas}  # TODO: add models, etc.
