from flask import url_for

from app import models


def test_getting_main_page_while_not_authenticated(client):
    response = client.get(
        url_for("main.index"),
        follow_redirects=False
    )
    assert response.status_code == 200


def test_getting_main_page_while_authenticated(auth, client, session):
    auth.login()
    user = session.get(models.User, 1)
    response = client.get(
        url_for("main.index", username=user.username),
        follow_redirects=False
    )
    assert response.status_code == 302
    profile_page = url_for("main.profile", username=user.username, _external=False)
    assert response.location[:len(profile_page)] == profile_page


def test_getting_userpage_while_not_authenticated(client):
    response = client.get(
        url_for("main.profile", username="not-a-real-user"),
        follow_redirects=False
    )
    assert response.status_code == 302
    login_page = url_for("auth.login", _external=False)
    assert response.location[:len(login_page)] == login_page


def test_getting_userpage_while_authenticated(auth, client, session):
    auth.login()
    user = session.get(models.User, 1)
    response = client.get(
        url_for("main.profile", username=user.username),
        follow_redirects=False
    )
    assert response.status_code == 200
    assert user.username in response.text


def test_capitalization_agnostic_user_profile_routing(auth, client, session):
    user = session.get(models.User, 1)
    auth.login()

    response = client.get(url_for("main.profile", username=user.username))
    assert response.status_code == 200

    response = client.get(url_for("main.profile", username=user.username.upper()))
    assert response.status_code == 200
