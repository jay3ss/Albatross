from pathlib import Path
from pelican import read_settings


class Settings:

    def __init__(self, user_file: Path | str | None = None) -> None:
        if not user_file:
            user_file = None
        self._user_file = user_file


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
