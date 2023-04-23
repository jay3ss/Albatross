from app import models
from app.helpers import users as uh


def test_register_success(session):
    # Test that the function returns True on successful registration

    # Call the register function with a valid username
    result = uh.register("john", "john@example.com", "password", session)
    # Assert that the result is True
    assert result is True

    # Check that the user is added to the database
    user = models.User.query.filter_by(username="john").first()
    assert user is not None
    assert user.username == "john"
    assert user.username_lower == "john"


def test_register_failure(session):
    # Test that the function returns False on failed registration

    # Call the register function with an invalid username (e.g., one that's
    # already taken)
    result = uh.register("test", "test@example.com", "password", session)
    # Assert that the result is False
    assert result is False

    # Check that there is still only one user by the name 'test'
    users = models.User.query.filter_by(username="test").all()
    assert len(users) == 1
