from app import create_app

from .fixtures import app, client
from .testing_configs import TestConfig


def test_config():
    assert not create_app().testing
    assert create_app(TestConfig).testing


def test_hello(client):
    response = client.get('/hello')
    assert response.data == b'Hello, World!'
