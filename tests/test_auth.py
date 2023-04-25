import string
from unittest.mock import patch

from flask import url_for
import pytest

from app import models


def test_register(client):
    registration_url = url_for("auth.register", _external=False)
    assert client.get(registration_url).status_code == 200
    assert not models.User.is_username_taken("non-existent-user")
    data = data = dict(
        username="non-existent-user",
        email="non-existent-email@example.com",
        password="password",
        password2="password",
    )
    response = client.post(
        registration_url, data=data, follow_redirects=False
    )
    assert models.User.is_username_taken("non-existent-user")
    assert response.status_code == 302


def test_registration_with_valid_usernames(client):
    endings = ["", "137", "_", "-", "こんにちは"]
    usernames = [f"user{end}" for end in endings]
    emails = [f"{username}@example.com" for username in usernames]
    password = "password"
    message = "Username must contain only alphanumeric characters"

    for username, email in zip(usernames, emails):
        data = dict(
            username=username, email=email, password=password, password2=password
        )
        response = client.post(url_for("auth.register"), data=data)

        assert message not in response.text


def test_registration_with_invalid_usernames(client):
    username = "user{char}"
    email = "user@example.com"
    password = "password"
    message = "Username must contain only alphanumeric characters"

    allowed_chars = "-_"
    for char in string.punctuation:
        if char not in allowed_chars:
            data = dict(
                username=username.format(char=char),
                email=email,
                password=password,
                password2=password,
            )
            response = client.post(url_for("auth.register"), data=data)

            if message:
                assert message in response.text


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
        ("test", "email@example.com", "password", "password", "already exists"),
    ),
)
def test_register_validate_input(client, username, email, password, password2, message):
    data = dict(username=username, email=email, password=password, password2=password2)
    response = client.post(url_for("auth.register"), data=data, follow_redirects=True)

    assert message in response.text


def test_register_email_already_exist(client):
    data = dict(
        username="user2379637",
        email="test@example.com",
        password="password",
        password2="password"
    )
    message = "Email is already taken."

    with patch.object(models.User, 'is_email_taken', return_value=True):
        response = client.post(url_for("auth.register"), data=data, follow_redirects=True)

    assert message in response.text


def test_redirect_when_trying_to_register_while_authenticated(client, auth):
    auth.login()

    response = client.get(url_for("auth.register"), follow_redirects=True)
    assert response.request.path == url_for("main.profile", username="test", _external=False)


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
        follow_redirects=True,
    )
    assert response.request.path == url_for("main.profile", username="test", _external=False)


def test_logout(auth):
    auth.login()

    response = auth.logout()
    assert response.status_code == 302


def test_register_case_insensitive_email(client, session):
    user = session.get(models.User, 1)
    data = dict(
        username="bill",
        email=user.email.upper(),
        password="cat",
        password2="cat"
    )
    response = client.post(
        url_for("auth.register"),
        data=dict(username="bill", email=user.email.upper(), password="password", password2="password")
    )
    assert "Email is already taken" in response.text
