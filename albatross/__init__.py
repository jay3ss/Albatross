from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from config import Config


db = SQLAlchemy()
migrate = Migrate()


def create_app(config_class: Config = Config) -> Flask:
    """
    Create and configure a Flask application.

    Args:
        config_class (Config): The configuration class to use for configuring
        the app.

    Returns:
        Flask: The configured Flask application object.
    """
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)

    return app


from albatross.core import models, schemas
