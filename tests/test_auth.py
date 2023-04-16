
import pytest
from flask import session, g
from flask_login import current_user

from app import db, models
from tests.fixtures import app, auth, client


def test_register(client, app):
    assert client.get('/auth/register').status_code == 200
    response = client.post(
        "/auth/register",
        data=dict(username="me", email="me@example.com", password="password")
    )
    assert response.headers.get("Location", None) == "/auth/login"

    # with app.app_context():
    #     assert

@pytest.mark.parametrize(('username', 'email', 'password', 'message'), (
    ('', '', '', b'Username is required.'),
    ('a', '', '', b'Password is required.'),
    ('test', 'test', 'test@example.com', b'already registered'),
))
def test_register_validate_input(client, username, email, password, message):
    response = client.post(
        '/auth/register',
        data=dict(username=username, email=email, password=password)
    )
    assert message in response.data


def test_login(client, auth):
    assert client.get('/auth/login').status_code == 200

    response = auth.login()
    assert response.status_code == 200 # NOTE: should it be 30x?

    with client:
        client.get('/')
        # assert current_user.is_authenticated
        assert session["user_id"] == 1
        assert g.user['username'] == 'test'


@pytest.mark.parametrize(('username', 'password', 'message'), (
    ('a', 'test', b'Incorrect username or password.'),
    ('test', 'a', b'Incorrect password or password.'),
))
def test_login_validate_input(auth, username, password, message):
    response = auth.login(username, password)
    assert message in response.data


def test_logout(client, auth):
    auth.login()

    with client:
        auth.logout()
        assert not current_user.is_authenticated


if __name__ == "__main__":
    import pytest
    pytest.main(["-s", __file__])
