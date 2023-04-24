from app.helpers import users as uh
from app.models import User, load_user


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
    assert User.is_username_taken('bill')
    assert User.is_username_taken('BILl')

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
