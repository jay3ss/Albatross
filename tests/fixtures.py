import pytest

from app import create_app, db, models
from .helpers import AuthActions
from .testing_configs import TestConfig


@pytest.fixture
def app():
    """App fixture"""
    app = create_app(TestConfig)

    app_context = app.app_context()
    app_context.push()
    db.create_all()

    # create the user in the database so we can log in
    u = models.User(username="test", email="test@example.com")
    u.set_password("password")
    db.session.add(u)
    db.session.commit()

    yield app

    db.session.remove()
    db.drop_all()
    app_context.pop()


@pytest.fixture
def client(app):
    """Test client fixture"""
    return app.test_client()


@pytest.fixture
def session(app):
    """Create a new database session for a test."""
    with app.app_context():
        yield db.session
        db.session.rollback()
        db.drop_all()


@pytest.fixture
def auth(client):
    """Authentication fixture"""
    return AuthActions(client)
