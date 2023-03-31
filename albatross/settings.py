import pathlib

from dotenv import load_dotenv
from pelican import read_settings
from pydantic import BaseSettings, Field


load_dotenv()


class Config(BaseSettings):
    # database settings
    database_uri: str = Field(..., env="DATABASE_URI")
    templates_dir: pathlib.Path = pathlib.Path(__file__).parent / "templates"

    # other settings
    # add other settings as needed


config = Config()


def get_user_settings() -> dict:
    """
    Retrieves the user's settings

    Returns:
        dict: the user's settings
    """
    user_settings = {}
    return user_settings


def get_settings() -> dict:
    """
    Retrieves the app's settings (including user settings)

    Returns:
        dict: the app's settings
    """
    settings = read_settings()
    settings.update(get_user_settings())
    return settings
