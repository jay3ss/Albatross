import json
from pathlib import Path

from werkzeug.datastructures import FileStorage

from app.settings import forms


def test_validating_proper_settings_file(app, settings_file):
    updated_data = {"SITENAME": "Test Site"}
    with open(settings_file, "w") as f:
        json.dump(updated_data, f)

    with app.app_context():
        form = forms.UserSettingsFileUploadForm(
            file=FileStorage(open(settings_file, "rb"))
        )
        assert form.validate()


def test_validating_empty_settings_file(app, settings_file):
    with open(settings_file, "w") as f:
        json.dump("", f)

    with app.app_context():
        form = forms.UserSettingsFileUploadForm(
            file=""
        )
        assert not form.validate()


def test_validating_invalid_settings_file(app, settings_file):
    with open(settings_file, "w") as f:
        f.write('"SITENAME": "A Site"')

    with app.app_context():
        form = forms.UserSettingsFileUploadForm(
            file=FileStorage(open(settings_file, "rb"))
        )
        assert not form.validate()


def test_validating_settings_file_with_incorrect_extension(app, tmp_path):
    settings_file = tmp_path / "user_settings.txt"
    with open(settings_file, "w") as f:
        json.dump({"SITENAME": "A Site"}, f)

    with app.app_context():
        form = forms.UserSettingsFileUploadForm(
            file=FileStorage(settings_file)
        )
        assert not form.validate()


if __name__ == "__main__":
    import pytest
    pytest.main(["-s", __file__])
