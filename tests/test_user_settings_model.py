import json
from pathlib import Path

from pelican import read_settings
import pytest

from app import models


def test_user_settings_model(session):
    pass


def test_get_settings_with_existing_settings(session, user):
    new_settings = models.UserSettings()
    new_settings.id = user.id
    models.save_settings(new_settings, session=session)

    settings = models.get_settings(user)
    assert isinstance(settings(), dict)
    assert settings()


def test_get_settings_with_non_existing_settings(session):
    settings = models.get_settings()
    assert isinstance(settings(), dict)


def test_save_settings_with_existing_entry(settings):
    pass


def test_save_settings_without_existing_entry(settings):
    pass


def test_load_settings(settings):
    assert settings == read_settings()


def test_create_settings_file(settings_file):
    assert not settings_file.exists()
    settings_file = models.UserSettings.create_settings_file(settings_file)
    assert settings_file.exists()


def test_modify_settings_with_file(settings_file):
    settings = models.UserSettings()
    with open(settings_file, "w") as f:
        json.dump({"SITENAME": "My Pelican Site"}, f)
    settings.update(settings_file)
    assert settings["SITENAME"] == "My Pelican Site"
    settings["SITENAME"] = "New Site Name"
    assert settings["SITENAME"] == "New Site Name"


def test_creating_settings_file(settings_file):
    settings_file = models.UserSettings.create_settings_file(settings_file)
    pelican_settings = read_settings()

    pelican_settings_json = "pelican_settings.json"
    with open(pelican_settings_json, "w") as f:
        json.dump(pelican_settings, f)

    with open(pelican_settings_json, "r") as f:
        pelican_settings = json.load(f)

    with open(settings_file, "r") as f:
        written_settings = json.load(f)

    assert pelican_settings == written_settings

    Path(pelican_settings_json).unlink()


def test_get_pelican_settings():
    default_settings = models.UserSettings._get_pelican_settings()
    assert isinstance(default_settings, dict)
    assert "SITENAME" in default_settings
    assert "OUTPUT_RETENTION" in default_settings


def test_merge_settings():
    settings = models.UserSettings()
    user_settings = {"SITENAME": "My New Site Name"}
    settings.update(user_settings)
    assert settings["SITENAME"] == "My New Site Name"


def test_get_settings(settings_file):
    models.UserSettings.create_settings_file(settings_file)
    settings = models.UserSettings(settings_file)
    settings.update({"SITENAME": "My New Site Name"})
    settings.write(settings_file)
    assert settings["SITENAME"] == "My New Site Name"
    assert settings["OUTPUT_PATH"] == "output"

    Path(settings_file).unlink()


def test_update_nested_settings():
    # Given
    settings = models.UserSettings()

    # When
    settings["JINJA_ENVIRONMENT"]["trim_blocks"] = False

    # Then
    assert settings["JINJA_ENVIRONMENT"]["trim_blocks"] == False


def test_update_nested_settings_with_list():
    # Given
    settings = models.UserSettings()

    # When
    settings["READERS"]["0.1"] = ""

    # Then
    assert settings["READERS"]["0.1"] == ""


def test_write_nested_settings(settings_file):
    # Given
    settings = models.UserSettings()
    settings["JINJA_ENVIRONMENT"]["trim_blocks"] = False

    # When
    settings.write(settings_file)

    # Then
    with open(settings_file) as f:
        user_settings = json.load(f)

    assert user_settings["JINJA_ENVIRONMENT"]["trim_blocks"] == False

    Path(settings_file).unlink()


def test_read_nested_settings(settings_file):
    # Given
    with open(settings_file, "w") as f:
        json.dump(
            {"JINJA_ENVIRONMENT": {"trim_blocks": False, "lstrip_blocks": True}}, f
        )

    settings = models.UserSettings()
    settings.update(settings_file)

    # Then
    assert settings["JINJA_ENVIRONMENT"]["trim_blocks"] == False
    assert settings["JINJA_ENVIRONMENT"]["lstrip_blocks"] == True

if __name__ == "__main__":
    import pytest
    pytest.main(["-s", __file__])
