import pytest

from app import create_app, db, models
from app.helpers import users as uh
from .helpers import AuthActions
from config import TestConfig


@pytest.fixture
def app():
    """App fixture"""
    app = create_app(TestConfig)

    app_context = app.app_context()
    app_context.push()
    db.create_all()

    # create the user in the database so we can log in
    uh.register(
        username="test",
        email="test@example.com",
        password="password",
        session=db.session,
    )

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
def user(session):
    return session.get(models.User, 1)


@pytest.fixture
def auth(client):
    """Authentication fixture"""
    return AuthActions(client)


@pytest.fixture
def article(session, user):
    """Fixture to create a sample article in the database for testing."""
    article = models.Article(
        title="Test Article", content="This is a test article content", user=user
    )
    session.add(article)
    session.commit()
    return article


# adapted from:
# https://github.com/wtforms/wtforms/blob/master/tests/conftest.py


@pytest.fixture
def dummy_form():
    return DummyForm()


@pytest.fixture
def dummy_field():
    return DummyField()


class DummyTranslations:
    def gettext(self, string):
        return string

    def ngettext(self, singular, plural, n):
        if n == 1:
            return singular

        return plural


class DummyField:
    _translations = DummyTranslations()

    def __init__(
        self,
        data=None,
        name=None,
        errors=(),
        raw_data=None,
        label=None,
        id=None,
        field_type="StringField",
    ):
        self.data = data
        self.name = name
        self.errors = list(errors)
        self.raw_data = raw_data
        self.label = label
        self.id = id if id else ""
        self.type = field_type

    def __call__(self, **other):
        return self.data

    def __str__(self):
        return self.data

    def __iter__(self):
        return iter(self.data)

    def _value(self):
        return self.data

    def iter_choices(self):
        return iter(self.data)

    def iter_groups(self):
        return []

    def has_groups(self):
        return False

    def gettext(self, string):
        return self._translations.gettext(string)

    def ngettext(self, singular, plural, n):
        return self._translations.ngettext(singular, plural, n)


class DummyForm(dict):
    pass


@pytest.fixture(scope="function")
def settings_file(tmp_path):
    settings_path = tmp_path / "user_settings.json"

    yield settings_path


@pytest.fixture
def settings(session, user):
    settings = models.UserSettings(user=user)
    session.add(settings)
    session.commit()

    return settings
