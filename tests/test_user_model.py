import unittest


from app import db, create_app, login
from app.models import User, load_user
from tests.testing_configs import TestConfig


class UserModelCase(unittest.TestCase):
    def setUp(self) -> None:
        self.app = create_app(TestConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self) -> None:
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_password_hashing(self) -> None:
        u = User(username="susan")
        u.set_password("cat")
        self.assertFalse(u.check_password("dog"))
        self.assertTrue(u.check_password("cat"))

    def test_string_representation(self):
        name = "susan"
        u = User(username=name)
        assert name in str(u)

    def test_loading_of_user(self):
        u = User(username="test", email="test@example.com")
        u.set_password("password")
        db.session.add(u)
        db.session.commit()
        loaded_user = load_user(u.id)

        assert loaded_user.id == u.id
