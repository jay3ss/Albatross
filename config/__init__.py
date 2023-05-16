import os
from pathlib import Path
from typing import Any, Callable

from dotenv import load_dotenv


load_dotenv()

base_dir = os.path.abspath(os.path.dirname(__file__))


def env_var(key: str, default: Any, type: Callable = None) -> Any:
    """
    Retrieve the value of an environment variable with a default value if not
    set.

    Args:
        key (str): The name of the environment variable to retrieve.
        default (Any): The default value to return if the environment variable
        is not set.
        type (Callable): If given, converts the value to the type. Default None.

    Returns:
        Any: The value of the environment variable if set, otherwise the default
        value.
    """
    if type:
        return type(os.environ.get(key, default=default))
    return os.environ.get(key, default=default)


class Config:
    DEBUG: bool = env_var("DEBUG", False)
    TESTING: bool = env_var("TESTING", False)
    SECRET_KEY: str = env_var("SECRET_KEY", "my-secret-key")
    SQLALCHEMY_DATABASE_URI = env_var(
        "DATABASE_URI", f"sqlite:///{os.path.join(base_dir, 'app.db')}"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS: bool = env_var("TRACK_MODIFICATIONS", False)
    BOOTSTRAP_BOOTSWATCH_THEME = "litera"
    ARTICLES_PER_PAGE = env_var("ARTICLES_PER_PAGE", 25)
    ADMINS = env_var("ADMINS", ["albatross@example.com"])
    # TODO: more MDEditor settings
    MDEDITOR_LANGUAGE = env_var("MDEDITOR_LANGUAGE", "en")
    MDEDITOR_FILE_UPLOADER = env_var(
        "MDEDITOR_FILE_UPLOADER", os.path.join(base_dir, "uploads")
    )
    MAX_CONTENT_LENGTH = env_var("MAX_CONTENT_LENGTH", 16 * 1_000 * 1_000, type=int)
    UPLOAD_FOLDER = env_var("UPLOAD_FOLDER", Path(base_dir).parent/"uploads")
    UPLOAD_EXTENSIONS = [".json"]


class TestConfig(Config):
    DEBUG = True
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    APPLICATION_ROOT = ""
    SERVER_NAME = "localhost.localdomain"
    WTF_CSRF_ENABLED = False
    ARTICLES_PER_PAGE = 10
