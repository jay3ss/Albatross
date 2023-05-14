# import json

# from pathlib import Path

# from pelican import read_settings
# from typing import Any


# class Settings:
#     def __init__(self, user_file: Path | str | None = None) -> None:
#         load_user_file = True
#         if not user_file:
#             user_file = Path("config/user_settings.json")
#             load_user_file = False

#         self._user_file = user_file
#         self._settings = Settings._get_pelican_settings()

#         if load_user_file:
#             with open(self._user_file, "r") as f:
#                 self._settings.update(json.load(f))

#     def __new__(cls, *args, **kwargs) -> "Settings":
#         """Only create a new instance if one hasn't already been created

#         Returns:
#             Settings: singleton Settings object
#         """
#         if not hasattr(cls, "instance"):
#             cls.instance = super(Settings, cls).__new__(cls, *args, **kwargs)
#         return cls.instance

#     def update(self, new_settings: dict | Path | str) -> "Settings":
#         """
#         Updates the settings with contents of the new settings

#         Args:
#             new_settings (dict | Path | str): Either a dict of the settings
#             to update the current settings with or a Path (str too) to the file
#             of new settings.

#         Returns:
#             Settings: the updated Settings instance.
#         """
#         if isinstance(new_settings, dict):
#             self._settings.update(new_settings)
#         else:
#             with open(new_settings, "r") as f:
#                 file_contents = json.loads(f.read())

#             self._settings.update(file_contents)

#         return self

#     def merge(self, settings) -> None:
#         """
#         Merge a UserSettings object with this object.

#         Args:
#             settings (UserSettings): the UserSettings object
#         """
#         self.id = settings.id
#         self.update(settings.to_dict())

#     def write(self, fname: Path | str = "user_settings.json") -> Path:
#         """
#         Writes the settings to the given file

#         Args:
#             fname (Path | str, optional): Path or filename to write
#             the settings to. Defaults to None. If None, the file will be in the
#             working directory in with the filename 'user_settings.json'

#         Returns:
#             Path: path to the file
#         """
#         return _write_dict_to_file(fname=fname, contents=self._settings)

#     def __str__(self) -> str:
#         return str(self._settings)

#     def __call__(self) -> dict:
#         return self._settings

#     @staticmethod
#     def create_settings_file(fname: Path | str | None = None) -> Path:
#         """
#         Creates the settings file with the given filename.

#         Args:
#             fname (Path | str | None, optional): Path or filename to write the
#             settings to. Defaults to None. If None, the file will be in the
#             working directory in with the filename 'user_settings.json'.
#             Defaults to None.

#         Returns:
#             Path: Path to the file
#         """
#         return _write_dict_to_file(fname=fname, contents=read_settings())

#     @staticmethod
#     def _get_pelican_settings(
#         path: Path | str | None = None, override: dict | None = None
#     ) -> dict:
#         """
#         Retrieves the app's settings (including user settings)

#         Args:
#             path (Path | str | None, optional): Path to the settings file.
#                 Defaults to None.
#             override (dict | None, optional): The settings to override and their
#             values. Defaults to None.

#         Returns:
#             dict: Pelican's settings
#         """
#         return read_settings(path=path, override=override)

#     def __eq__(self, other_settings: dict) -> bool:
#         return self._settings == other_settings

#     def __getitem__(self, index) -> Any:
#         return self._settings[index]

#     def __setitem__(self, index, value) -> None:
#         self._settings[index] = value


# def _write_dict_to_file(fname: Path | str | None, contents: dict) -> Path:
#     """
#     Writes the contents to a file with the given name

#     Args:
#         Args:
#         fname (Path | str | None, optional): Path or filename to write the
#             settings to. Defaults to None. If None, the file will be in the
#             working directory in with the filename 'user_settings.json'.
#             Defaults to None.
#         contents (dict): the dict to write to the file

#     Returns:
#         Path: Path to the file
#     """
#     if not isinstance(fname, Path):
#         fname = Path(fname)

#     with open(fname, "w") as f:
#         json.dump(contents, f)

#     return fname
