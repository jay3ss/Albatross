from time import sleep

from app.helpers import users as uh
from app.models import Article, User, load_user


def test_password_hashing(session):
    uh.register("bill", "bill@example.com", "cat", session)
    u = User.query.filter_by(username="bill").first()

    assert not u.check_password("dog")
    assert u.check_password("cat")


def test_string_representation():
    name = "susan"
    u = User(username=name)
    assert name in str(u)


def test_loading_of_user(app):
    user_id = 1
    loaded_user = load_user(user_id)

    assert loaded_user.id == user_id


def test_username_uniqueness(session):
    # Create a user
    result = uh.register("Bill", "bill@example.com", "password", session)
    assert result

    # Attempt to create another user with the same username (different
    # capitalization)
    result = uh.register("BiLl", "bill@example.com", "password", session)
    assert not result


def test_username_uniqueness_case_insensitive(session):
    # Create a user
    result = uh.register("Bill", "bill@example.com", "password", session)
    assert result

    result = uh.register("bILL", "william@example.com", "password", session)
    assert not result

    # Check if the username is unique (case-insensitive)
    assert User.is_username_taken("bILL")
    assert User.is_username_taken("bill")
    assert User.is_username_taken("BILl")

def test_email_uniqueness(session):
    user = session.get(User, 1)

    assert User.is_email_taken(user.email)
    assert not User.is_email_taken("blah@blah.com")


def test_email_uniqueness_case_insensitive(session):
    # Create a user
    user = session.get(User, 1)

    # Check if the email is unique (case-insensitive)
    assert User.is_email_taken(user.email.upper())
    assert User.is_email_taken(user.email.capitalize())
    assert User.is_email_taken("TeSt@ExAmPlE.com")


def test_generate_slug_before_insert(session):
    user = User(username="JohnDoe", email="jd@example.com")
    session.add(user)
    session.commit()

    assert user.username_lower == "johndoe"

def test_generate_slug_before_update(session):
    user = User(username="JohnDoe", email="jd@example.com")
    session.add(user)
    session.commit()

    user.username = "JaneDoe"
    session.commit()

    assert user.username_lower == "janedoe"


def test_generate_slug_before_update(session):
    user = User(username="JohnDoe", email="jd@example.com")
    session.add(user)
    session.commit()

    updated_at = user.updated_at

    user.username = "JaneDoe"
    session.commit()

    assert user.updated_at is not None
    assert updated_at < user.updated_at


def test_num_drafts():
    # Create a test User object
    user = User()

    # Create some test articles
    article1 = Article(is_draft=True)
    article2 = Article(is_draft=True)
    article3 = Article(is_draft=False)

    # Add articles to user's articles list
    user.articles = [article1, article2, article3]

    # Test num_drafts property
    assert user.num_drafts == 2  # Expect 2 drafts

def test_num_published():
    # Create a test User object
    user = User()

    # Create some test articles
    article1 = Article(is_draft=True)
    article2 = Article(is_draft=True)
    article3 = Article(is_draft=False)

    # Add articles to user's articles list
    user.articles = [article1, article2, article3]

    # Test num_published property
    assert user.num_published == 1  # Expect 1 published article


def test_get_reset_password_token(session):
    user = session.get(User, 1)

    token = user.get_reset_password_token()
    assert isinstance(token, str)

    user_should_not_be_none = User.verify_reset_password_token(token)
    assert user_should_not_be_none == user


def test_verify_reset_password_token(session):
    user = session.get(User, 1)

    token = user.get_reset_password_token(expires_in=0.0001)
    sleep(0.00011)
    user_should_be_none = User.verify_reset_password_token(token)
    assert user_should_be_none is None


if __name__ == "__main__":
    import pytest
    pytest.main(["-s", __file__])
