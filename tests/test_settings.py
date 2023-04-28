import json
from pathlib import Path

from pelican import read_settings
import pytest

from config.settings import Settings


@pytest.fixture(scope="function")
def settings_file(tmp_path):
    settings_path = tmp_path / "user_settings.json"

    yield settings_path


def test_load_settings(settings):
    assert settings == read_settings()


def test_create_settings_file(settings_file):
    assert not settings_file.exists()
    settings_file = Settings.create_settings_file(settings_file)
    assert settings_file.exists()


def test_modify_settings_with_file(settings_file):
    settings = Settings()
    with open(settings_file, "w") as f:
        json.dump({"SITENAME": "My Pelican Site"}, f)
    settings.update(settings_file)
    assert settings["SITENAME"] == "My Pelican Site"
    settings["SITENAME"] = "New Site Name"
    assert settings["SITENAME"] == "New Site Name"


def test_creating_settings_file(settings_file):
    settings_file = Settings.create_settings_file(settings_file)
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
    Path(settings_file).unlink()
    # settings = Settings(settings_file)
    # assert settings["SITENAME"] == "My Pelican Site"
    # settings.update({"SITENAME": "New Site Name"})
    # settings.write(settings_file)
    # with open(settings_file) as f:
    #     saved_settings = json.load(f)
    # assert saved_settings["SITENAME"] == "New Site Name"


def test_get_pelican_settings():
    default_settings = Settings._get_pelican_settings()
    assert isinstance(default_settings, dict)
    assert "SITENAME" in default_settings
    assert "OUTPUT_RETENTION" in default_settings


def test_merge_settings():
    settings = Settings()
    user_settings = {"SITENAME": "My New Site Name"}
    settings.update(user_settings)
    assert settings["SITENAME"] == "My New Site Name"


def test_get_settings(settings_file):
    Settings.create_settings_file(settings_file)
    settings = Settings(settings_file)
    settings.update({"SITENAME": "My New Site Name"})
    settings.write(settings_file)
    assert settings["SITENAME"] == "My New Site Name"
    assert settings["OUTPUT_PATH"] == "output"

    Path(settings_file).unlink()


def test_update_nested_settings():
    # Given
    settings = Settings()

    # When
    settings["JINJA_ENVIRONMENT"]["trim_blocks"] = False

    # Then
    assert settings["JINJA_ENVIRONMENT"]["trim_blocks"] == False


def test_update_nested_settings_with_list():
    # Given
    settings = Settings()

    # When
    settings["READERS"]["0.1"] = ""

    # Then
    assert settings["READERS"]["0.1"] == ""


def test_write_nested_settings(settings_file):
    # Given
    settings = Settings()
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
        json.dump({
            "JINJA_ENVIRONMENT": {
                "trim_blocks": False,
                "lstrip_blocks": True
            }
        }, f)

    settings = Settings()
    settings.update(settings_file)

    # Then
    assert settings["JINJA_ENVIRONMENT"]["trim_blocks"] == False
    assert settings["JINJA_ENVIRONMENT"]["lstrip_blocks"] == True


if __name__ == "__main__":
    pytest.main(["-s", __file__])
