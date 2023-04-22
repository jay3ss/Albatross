"""
https://flask.palletsprojects.com/en/2.2.x/templating/#context-processors

Adapted from:
https://abstractkitchen.com/blog/how-to-create-custom-jinja-filters-in-flask/
"""

from flask import Flask


def register_context_processor(app: Flask) -> None:

    @app.context_processor
    def inject_is_production() -> dict:
        return dict(
            application_name="Flask-Backbone"
        )
