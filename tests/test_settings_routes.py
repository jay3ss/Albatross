import json
from pathlib import Path

from flask import current_app, url_for
from werkzeug.datastructures import FileStorage
from wtforms.fields.simple import FileField

from app import models


def test_can_access_settings_while_authenticated(auth, client, settings):
    auth.login()

    response = client.get(url_for("settings.settings"))

    assert response.status_code == 200


def test_can_access_settings_while_not_authenticated(client):
    response = client.get(
        url_for("settings.settings"),
        follow_redirects=False
    )

    assert response.status_code == 302
    login_url = url_for("auth.login", _external=False)
    assert response.headers.get("Location", None)[:len(login_url)] == login_url


def test_writing_settings_to_file_while_not_authenticated(client):
    response = client.post(
        url_for("settings.export"),
        follow_redirects=False
    )

    assert response.status_code == 302
    login_url = url_for("auth.login", _external=False)
    assert response.headers.get("Location", None)[:len(login_url)] == login_url


def test_writing_settings_to_file(auth, client, settings, user):
    auth.login()

    response = client.post(
        url_for("settings.export"),
        follow_redirects=False
    )

    assert response.status_code == 200
    upload_dir = Path(current_app.config["UPLOAD_FOLDER"])
    settings_file_path = (upload_dir/ f"{user.username_lower}-settings.json").resolve()
    assert settings_file_path.exists()

    settings_file_path.unlink()


def test_attempting_to_upload_while_not_authenticated(client):
    response = client.post(
        url_for("settings.upload_settings"),
        follow_redirects=False
    )

    assert response.status_code == 302
    login_url = url_for("auth.login", _external=False)
    assert response.headers.get("Location", None)[:len(login_url)] == login_url


def test_attempting_to_upload_while_authenticated(auth, client):
    auth.login()
    response = client.post(
        url_for("settings.upload_settings"),
        follow_redirects=False
    )

    assert response.status_code == 302
    settings_url = url_for("settings.settings", _external=False)
    assert response.headers.get("Location", None)[:len(settings_url)] == settings_url


def test_attempting_to_upload_valid_settings_file(app, auth, client, settings, user):
    json_file = f"{user.username}_settings.json"
    with open(json_file, "w") as f:
        json.dump({"SITENAME": "A Site"}, f)


    data = {
        "file": FileStorage(
            stream=open(json_file, "rb"),
            filename=json_file
        ),
        "submit": True
    }
    with app.test_request_context():
        auth.login()
        response = client.post(
            url_for("settings.upload_settings"),
            data=data,
            follow_redirects=False
        )

    assert response.status_code == 302
    settings_url = url_for("settings.settings", _external=False)
    assert response.headers.get("Location", None)[:len(settings_url)] == settings_url

    Path(json_file).unlink()


if __name__ == "__main__":
    import pytest
    pytest.main(["-s", __file__])
