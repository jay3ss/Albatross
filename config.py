from dotenv import load_dotenv
from pydantic import BaseConfig, Field


load_dotenv()


class Config(BaseConfig):
    database_uri: str = Field(env="DATABASE_URI")
    debug: bool = Field(default=False, env="DEBUG")
    secret_key: str = Field(..., env="SECRET_KEY")
    SQLALCHEMY_DATABASE_URI: str = Field(env="DATABASE_URI")

    # other settings
    # add other settings as needed


config = Config()
