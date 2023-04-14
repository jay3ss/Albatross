# import pytest
# from flask import url_for
# from flask_login import current_user
# from werkzeug.security import generate_password_hash

# from app import create_app, db
# from app.models import User
# import config


# class TestConfig(config.Config):
#     testing = True
#     SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"


# @pytest.fixture(scope="module")
# def app():
#     """Fixture to create Flask app for testing."""
#     app = create_app(TestConfig)
#     with app.app_context():
#         db.create_all()
#         yield app
#         db.session.remove()
#         db.drop_all()


# @pytest.fixture(scope="module")
# def client(app):
#     """Fixture to create Flask test client."""
#     return app.test_client()


# @pytest.fixture(scope="module")
# def authenticated_client(client):
#     """Fixture to create authenticated Flask test client."""
#     # Create a test user
#     user = User(username="testuser", email="testuser@example.com")
#     password = "password"
#     user.set_password(password)
#     db.session.add(user)
#     db.session.commit()

#     # Log in the test user
#     client.post(
#         url_for("auth.login"),
#         data=dict(
#             username="testuser",
#             email="testuser@example.com",
#             password_hash=generate_password_hash(password),
#         ),
#         follow_redirects=True,
#     )

#     return client


# def test_login_page(client):
#     """Test login page template."""
#     response = client.get(url_for("auth.login"))
#     assert response.status_code == 200
#     assert b"Login" in response.data


# def test_login_functionality(client, authenticated_client):
#     """Test login functionality."""
#     # Test login with valid credentials
#     response = client.post(
#         url_for("auth.login"),
#         data=dict(username="testuser", password="password"),
#         follow_redirects=True,
#     )
#     assert response.status_code == 200
#     assert current_user.username == "testuser"

#     # Test login with invalid credentials
#     response = client.post(
#         url_for("auth.login"),
#         data=dict(username="testuser", password="wrongpassword"),
#         follow_redirects=True,
#     )
#     assert response.status_code == 200
#     assert b"Invalid username or password" in response.data


# def test_logout_functionality(client, authenticated_client):
#     """Test logout functionality."""
#     response = client.get(url_for("auth.logout"), follow_redirects=True)
#     assert response.status_code == 200
#     assert current_user.is_anonymous
#     assert b"Login" in response.data


# if __name__ == "__main__":
#     pytest.main(["-s", __file__])
import unittest
from flask import url_for
from flask_login import current_user
from werkzeug.security import generate_password_hash

from app import create_app, db
from app.models import User
import config


class TestConfig(config.Config):
    testing = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    APPLICATION_ROOT = ""
    SERVER_NAME = "localhost"


class TestAuthRoutes(unittest.TestCase):
    def setUp(self):
        """Set up Flask app, test client, and database for testing."""
        self.app = create_app(TestConfig)
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

        # Create a test user
        self.user = User(username="testuser", email="testuser@example.com")
        self.password = "password"
        self.user.set_password(self.password)
        # db.session.add(self.user)
        # db.session.commit()

        # Log in the test user
        # self.client.post(
        #     url_for("auth.login"),
        #     data=dict(
        #         username="testuser",
        #         email="testuser@example.com",
        #         password_hash=generate_password_hash(password),
        #     ),
        #     follow_redirects=True,
        # )

    def tearDown(self):
        """Clean up Flask app, test client, and database after testing."""
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_login_page(self):
        """Test login page template."""
        response = self.client.get(url_for("auth.login"))
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Login", response.data)

    def test_login_functionality(self):
        """Test login functionality."""
        # Test login with valid credentials
        username = self.user.username
        password = self.password
        response = self.client.post(
            url_for("auth.login"),
            data=dict(username=username, password=password),
            follow_redirects=True,
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(current_user.username, "testuser")

        # Test login with invalid credentials
        response = self.client.post(
            url_for("auth.login"),
            data=dict(username="testuser", password="wrongpassword"),
            follow_redirects=True,
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Invalid username or password", response.data)

    def test_logout_page(self):
        """Test logout page."""
        response = self.client.get(url_for('auth.login'))

        # Assert that the response resulted in a redirect
        self.assertRedirects(response, url_for('auth.login'), status_code=302)
        # self.assertEqual(response.location, url_for('auth.login', _external=True))

    def test_logout_functionality(self):
        """Test logout functionality."""
        response = self.client.get(url_for("auth.logout"), follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(current_user.is_anonymous)
        self.assertIn(b"Logout", response.data)

    # def test_login_page_redirect(self):
        # response = self.client.get(url_for('auth.login'))

        # Assert that the response resulted in a redirect
        # self.assertRedirects(response, url_for('auth.login'), status_code=302)
        # self.assertEqual(response.location, url_for('auth.login', _external=True))


if __name__ == "__main__":
    import pytest
    pytest.main(["-s", __file__])
