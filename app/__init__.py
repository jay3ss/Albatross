from flask import Flask
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from config import Config


db = SQLAlchemy()
login = LoginManager()
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
    login.init_app(app)
    migrate.init_app(app, db)


    from app.auth import bp as auth_bp


    app.register_blueprint(auth_bp, url_prefix="/auth")

    return app


from app import models
