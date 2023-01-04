from dotenv import load_dotenv

from pydantic import BaseSettings, Field


load_dotenv()


class Config(BaseSettings):
    # database settings
    database_uri: str = Field(..., env="DATABASE_URI")

    # other settings
    # add other settings as needed


config = Config()
