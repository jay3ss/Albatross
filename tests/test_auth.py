import flask
from flask import url_for
import pytest

from tests.fixtures import app, auth, client


def test_register(client):
    registration_url = url_for("auth.register", _external=False)
    assert client.get(registration_url).status_code == 200

    data = data = dict(
        username="non-existent-user",
        email="non-existent-email@example.com",
        password="password",
        password2="password",
    )
    response = client.post(registration_url, data=data)
    assert response.status_code == 302


@pytest.mark.parametrize(
    ("username", "email", "password", "password2", "message"),
    (
        ("", "", "", "", "This field is required."),
        ("a", "", "", "", "This field is required."),
        ("", "a", "", "", "Invalid email address."),
        ("", "", "a", "", "This field is required."),
        ("", "", "", "a", "This field is required."),
        ("a", "a", "", "", "This field is required."),
        ("a", "a@example", "", "", "This field is required."),
        ("a", "a@example", "asdf", "", "This field is required."),
        ("a", "a@example", "", "asdf", "This field is required."),
        ("test", "test@example.com", "password", "password", "already exists"),
        ("test", "email@example.com", "password", "password", "already exists"),
        ("username", "test@example.com", "password", "password", "already exists"),
    ),
)
def test_register_validate_input(client, username, email, password, password2, message):
    data = dict(username=username, email=email, password=password, password2=password2)
    response = client.post(url_for("auth.register"), data=data, follow_redirects=True)

    assert message in response.text


def test_redirect_when_trying_to_register_while_authenticated(client, auth):
    auth.login()

    response = client.get(url_for("auth.register"), follow_redirects=True)
    assert response.request.path == url_for("main.index", _external=False)


def test_login(client, auth):
    assert client.get("/auth/login").status_code == 200

    response = auth.login()
    assert response.status_code == 200


@pytest.mark.parametrize(
    ("username", "password", "message"),
    (
        ("a", "test", "Incorrect username or password."),
        ("test", "a", "Incorrect username or password."),
        ("test", "password", "Home"),
    ),
)
def test_login_validate_input(client, username, password, message):
    response = client.post(
        url_for("auth.login"),
        data=dict(username=username, password=password),
        follow_redirects=True,
    )
    assert message in response.text


def test_redirection_after_successful_login(client):
    response = client.post(
        url_for("auth.login"),
        data=dict(username="test", password="password"),
        follow_redirects=True
    )
    assert response.request.path == url_for("main.index", _external=False)


def test_logout(auth):
    auth.login()

    response = auth.logout()
    assert response.status_code == 302
