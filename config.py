import os
from typing import Any

from dotenv import load_dotenv


load_dotenv()

base_dir = os.path.abspath(os.path.dirname(__file__))


def env_var(key: str, default: Any) -> Any:
    """
    Retrieve the value of an environment variable with a default value if not
    set.

    Args:
        key (str): The name of the environment variable to retrieve.
        default (Any): The default value to return if the environment variable
        is not set.

    Returns:
        Any: The value of the environment variable if set, otherwise the default
        value.
    """
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


class TestConfig(Config):
    DEBUG = True
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    APPLICATION_ROOT = ""
    SERVER_NAME = "localhost.localdomain"
    WTF_CSRF_ENABLED = False
