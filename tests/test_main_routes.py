from unittest.mock import patch

from flask import url_for
import pytest

from app import models
from app.helpers import users as uh


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


def test_updating_user_update_everything(auth, client, session):
    user = session.get(models.User, 1)

    username = "new_username"
    about = "This is the 'about' text"
    email = "test@example.com"
    password = "new_password"
    auth.login()
    response = client.post(
        url_for("main.update_profile", username=user.username),
        data=dict(
            username=username,
            about=about,
            email=email,
            password=password,
            password2=password,
        ),
        follow_redirects=False
    )

    assert response.status_code == 302

    updated_user = session.get(models.User, 1)
    assert updated_user.username == user.username
    assert updated_user.email == email
    assert updated_user.about == about
    assert updated_user.check_password(password)


    # having the same username shouldn't trigger an error
    response = client.post(
        url_for("main.update_profile", username=username),
        data=dict(username="user"),
        follow_redirects=False
    )

    assert response.status_code == 200


def test_update_profile_while_not_authenticated(client, session):
    user = session.get(models.User, 1)
    response = client.get(
        url_for("main.profile", username=user.username, _external=False),
        follow_redirects=False
    )

    login_url = url_for("auth.login", _external=False)
    assert response.location[:len(login_url)] == login_url
    assert response.status_code == 302


def test_update_profile_update_only_username(auth, client, session):
    auth.login()
    username = "new_username"
    password = "password"
    user = session.get(models.User, 1)
    data = dict(
        username=username,
        email=user.email,

    )
    response = client.post(
        url_for("main.update_profile", username=user.username),
        data=data,
        follow_redirects=False
    )

    assert response.status_code == 302

    updated_user = session.get(models.User, 1)
    assert updated_user.username == username


def test_updating_user_email_only(auth, client, session):
    user = session.get(models.User, 1)

    email = "test@example.com"
    auth.login()
    response = client.post(
        url_for("main.update_profile", username=user.username),
        data=dict(
            username=user.username,
            email=email
        ),
        follow_redirects=False
    )

    assert response.status_code == 302
    updated_user = session.get(models.User, 1)
    assert updated_user.username == user.username
    assert updated_user.email == email


def test_updating_user_about_only(auth, client, session):
    user = session.get(models.User, 1)

    about = "this is the 'about' text"
    auth.login()
    response = client.post(
        url_for("main.update_profile", username=user.username),
        data=dict(
            username=user.username,
            email=user.email,
            about=about
        ),
        follow_redirects=False
    )

    assert response.status_code == 302
    updated_user = session.get(models.User, 1)
    assert updated_user.username == user.username
    assert updated_user.email == user.email
    assert updated_user.about == about


def test_updating_user_password_only(auth, client, session):
    user = session.get(models.User, 1)

    password = "new_password"
    auth.login()
    response = client.post(
        url_for("main.update_profile", username=user.username),
        data=dict(
            username=user.username,
            email=user.email,
            password=password,
            password2=password
        ),
        follow_redirects=False
    )

    assert response.status_code == 302
    updated_user = session.get(models.User, 1)
    assert updated_user.username == user.username
    assert updated_user.email == user.email
    assert updated_user.check_password(password)


def test_updating_email_to_existing_email(auth, client, session):
    username = "different"
    email = "another@example.com"
    password = "password"
    new_user = models.User(username=username, email=email)
    new_user.set_password(password)
    session.add(new_user)
    session.commit()

    old_user = session.get(models.User, 1)

    auth.login(username=new_user.username, password=password)
    response = client.post(
        url_for("main.update_profile", username=new_user.username),
        data=dict(
            username=new_user.username,
            email=old_user.email,
        ),
        follow_redirects=False
    )

    assert "Email is already taken" in response.text


def test_updating_username_to_existing_username(auth, client, session):
    username = "different"
    email = "another@example.com"
    password = "password"
    new_user = models.User(username=username, email=email)
    new_user.set_password(password)
    session.add(new_user)
    session.commit()

    old_user = session.get(models.User, 1)

    auth.login(username=new_user.username, password=password)
    response = client.post(
        url_for("main.update_profile", username=new_user.username),
        data=dict(
            username=old_user.username,
            email=new_user.email,
        ),
        follow_redirects=False
    )

    assert "Username is already taken" in response.text


def test_attempting_to_compile_while_not_authenticated(client, user):
    response = client.get(
        url_for("main.compile_site", username=user.username),
        follow_redirects=False
    )

    assert response.status_code == 302
    login_url = url_for("auth.login", _external=False)
    assert response.headers.get("Location", None)[:len(login_url)] == login_url


def test_attempting_to_compile_while_authenticated(auth, client, user):
    auth.login()

    response = client.get(
        url_for("main.compile_site", username=user.username),
        follow_redirects=False
    )

    assert response.status_code == 200


def test_attempting_to_compile_for_non_existent_user(auth, client, user):
    auth.login()

    response = client.get(
        url_for("main.compile_site", username="user_does_not_exist"),
        follow_redirects=False
    )

    assert response.status_code == 302
    profile_url = url_for("main.profile", username=user.username, _external=False)
    assert response.headers.get("Location", None)[:len(profile_url)] == profile_url


def test_attempting_to_compile_for_different_user(auth, client, session, user):
    new_user = models.User(username="new_user", email="new_user@example.com")
    new_user.set_password("password")
    session.add(new_user)
    session.commit()

    auth.login()

    response = client.get(
        url_for("main.compile_site", username=new_user.username),
        follow_redirects=False
    )

    assert response.status_code == 302
    index_url = url_for("main.index", _external=False)
    assert response.headers.get("Location", None)[:len(index_url)] == index_url


def test_attempting_to_compile_for_owning_user(auth, client, user):
    auth.login()

    response = client.get(
        url_for("main.compile_site", username=user.username),
        follow_redirects=False
    )

    assert response.status_code == 200
