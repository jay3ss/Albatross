import pytest

from app import create_app, db
from .helpers import AuthActions
from .testing_configs import TestConfig


@pytest.fixture
def app():
    """App fixture"""
    app = create_app(TestConfig)

    app_context = app.app_context()
    app_context.push()
    db.create_all()

    yield app

    db.session.remove()
    db.drop_all()
    app_context.pop()


@pytest.fixture
def client(app):
    """Test client fixture """
    return app.test_client()


@pytest.fixture
def auth(client):
    """Authentication fixture"""
    return AuthActions(client)
