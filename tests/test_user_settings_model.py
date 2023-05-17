import json
from pathlib import Path

import pytest
from pelican import read_settings

from app import models
from app.settings import current_settings


def test_load_settings(settings):
    def sort_by_key(e) -> bool: return e[0]
    assert sorted(settings.to_dict(), key=sort_by_key) == sorted(read_settings(), key=sort_by_key)


def test_create_settings_file(settings_file):
    assert not settings_file.exists()
    settings_file = models.UserSettings.create_settings_file(settings_file)
    assert settings_file.exists()


def test_modify_settings_with_file(settings, settings_file):
    with open(settings_file, "w") as f:
        json.dump({"SITENAME": "My Pelican Site"}, f)
    settings.update(settings_file)
    assert settings.get("SITENAME") == "My Pelican Site"
    settings.set("SITENAME", "New Site Name")
    assert settings.get("SITENAME") == "New Site Name"


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


def test_merge_settings(settings):
    user_settings = {"SITENAME": "My New Site Name"}
    settings.update(user_settings)
    assert settings.get("SITENAME") == "My New Site Name"


# def test_get_settings(settings_file):
#     models.UserSettings.create_settings_file(settings_file)
#     settings = models.UserSettings(settings_file)
#     settings.update({"SITENAME": "My New Site Name"})
#     settings.write(settings_file)
#     assert settings["SITENAME"] == "My New Site Name"
#     assert settings["OUTPUT_PATH"] == "output"

#     Path(settings_file).unlink()


def test_update_nested_settings(settings):
    # When
    jinja_env = settings.get("JINJA_ENVIRONMENT")
    jinja_env["trim_blocks"] = False
    settings.set("JINJA_ENVIRONMENT", jinja_env)

    # Then
    assert settings.get("JINJA_ENVIRONMENT")["trim_blocks"] == False


def test_update_nested_settings_with_list(settings):
    # When
    readers = settings.get("READERS")
    readers["0.1"] = ""
    settings.set("READERS", readers)
    # Then
    assert settings.get("READERS")["0.1"] == ""


def test_write_nested_settings_with_file_name(settings, settings_file):
    # Given
    jinja_env = settings.get("JINJA_ENVIRONMENT")
    jinja_env["trim_blocks"] = False
    settings.set("JINJA_ENVIRONMENT", jinja_env)

    # When
    settings.write(str(settings_file))

    # Then
    with open(settings_file) as f:
        user_settings = json.load(f)

    assert user_settings["JINJA_ENVIRONMENT"]["trim_blocks"] == False

    Path(settings_file).unlink()


def test_write_nested_settings_with_path(settings, settings_file):
    # Given
    jinja_env = settings.get("JINJA_ENVIRONMENT")
    jinja_env["trim_blocks"] = False
    settings.set("JINJA_ENVIRONMENT", jinja_env)

    # When
    settings.write(settings_file)

    # Then
    with open(settings_file) as f:
        user_settings = json.load(f)

    assert user_settings["JINJA_ENVIRONMENT"]["trim_blocks"] == False

    Path(settings_file).unlink()


def test_read_nested_settings(settings, settings_file):
    # Given
    with open(settings_file, "w") as f:
        json.dump(
            {"JINJA_ENVIRONMENT": {"trim_blocks": False, "lstrip_blocks": True}}, f
        )

    settings.update(settings_file)

    # Then
    assert settings.get("JINJA_ENVIRONMENT")["trim_blocks"] == False
    assert settings.get("JINJA_ENVIRONMENT")["lstrip_blocks"] == True


def test_current_settings(app, auth, settings):
    auth.login()
    with app.app_context():
        current_settings == settings


def test_current_settings_not_authenticated(app):
    with app.app_context():
        assert current_settings == None


if __name__ == "__main__":
    import pytest
    pytest.main(["-s", __file__])
