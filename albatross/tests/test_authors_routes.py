from http import HTTPStatus
import unittest
from unittest import mock

from flask.testing import FlaskClient

from albatross import create_app
from albatross.core import models, schemas
import config


class TestConfig(config.Config):
    testing: bool = True
    SQLALCHEMY_DATABASE_URI: str = "sqlite://"


class TestAuthorsRoutes(unittest.TestCase):

    def setUp(self) -> None:
        self.app = create_app(config_class=TestConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.client = self.app.test_client()

    @mock.patch("albatross.helpers.database.get_author_by_id")
    def test_get_existing_author(self, mock_get_author):
        author_id = 1
        mock_author = schemas.Author(id=author_id, name="John Doe")
        mock_get_author.return_value = mock_author

        response = self.client.get(f"/authors/{author_id}")

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.headers["content-type"], "text/html; charset=utf-8")

        rendered_template = response.text.decode("utf-8")
        self.assertIn(mock_author.name, rendered_template)

        mock_get_author.assert_called_once_with(author_id=author_id)



    @mock.patch("albatross.helpers.database.get_author_by_id")
    def test_get_existing_author(self, mock_get_author):
        author_id = 1
        mock_author = schemas.Author(id=author_id, name="John Doe")
        mock_get_author.return_value = mock_author

        response = self.client.get(f"/authors/{author_id}")

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.headers["content-type"], "text/html; charset=utf-8")

        rendered_template = response.text.decode("utf-8")
        self.assertIn(mock_author.name, rendered_template)

        mock_get_author.assert_called_once_with(author_id=author_id)


    @mock.patch("albatross.helpers.database.get_author_by_id")
    def test_get_nonexistent_author(self, mock_get_author):
        mock_author = None
        mock_get_author.return_value = mock_author
        author_id = 1

        response = self.client.get(f"/authors/{author_id}")
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
        # assert response.json() == {"detail": "Author not found"}

        mock_get_author.assert_called_once_with(author_id=author_id)


    @mock.patch("albatross.helpers.database.get_authors")
    def test_get_all_authors_no_limit(self, mock_get_authors):
        mock_authors = [
            models.Author(name="Author 1"),
            models.Author(name="Author 2")
        ]
        mock_get_authors.return_value = mock_authors

        response = self.client.get("/authors")

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.headers["content-type"], "text/html; charset=utf-8")

        rendered_template = response.text.decode("utf-8")
        self.assertIn("Author 1", rendered_template)
        self.assertIn("Author 2", rendered_template)

        mock_get_authors.assert_called_once_with(limit=None)


    @mock.patch("albatross.helpers.database.get_authors")
    def test_get_all_authors_limit_5(self, mock_get_authors):
        limit = 5
        mock_authors = [models.Author(name=f"Author {i}") for i in range(1, limit+1)]
        mock_get_authors.return_value = mock_authors

        response = self.client.get("/authors", params={"limit": 5})

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.headers["content-type"], "text/html; charset=utf-8")

        rendered_template = response.text.decode("utf-8")
        for author in mock_authors:
            self.assertIn(author.name, rendered_template)

        mock_get_authors.assert_called_once_with(limit=limit)


    @mock.patch("albatross.helpers.database.create_author")
    def test_create_author(self, mock_create_author):
        mock_author = models.Author(name="Jane Doe", id=1)
        mock_create_author.return_value = mock_author
        new_author = schemas.Author(name=mock_author.name, id=mock_author.id)

        response = self.client.post("/authors/new", json=new_author.dict())
        self.assertEqual(response.status_code, HTTPStatus.CREATED)
        # assert response.json()["name"] == new_author.name
        # assert response.json()["id"] == mock_author.id

        mock_create_author.assert_called_once_with(
            schemas.AuthorCreate(name="Jane Doe")
        )

    def test_new_author(self):
        response = self.client.get("/authors/new")

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.headers["content-type"], "text/html; charset=utf-8")
        self.assertEqual(b"<form", response.text)

    @mock.patch("albatross.helpers.database.update_author")
    def test_update_author(self, mock_update_author):
        author_id = 1
        new_name = "New Name"
        mock_updated_author = models.Author(name=new_name, id=author_id)
        mock_update_author.return_value = mock_updated_author

        author_update = schemas.AuthorUpdate(name=new_name, id=author_id)

        response = self.client.post(f"/authors/{author_id}", json=author_update.dict())
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.headers["content-type"], "text/html; charset=utf-8")
        # assert response.json()["author"] == {"name": new_name, "id": author_id}

        mock_update_author.assert_called_once_with(author=author_update)

    @mock.patch("albatross.helpers.database.update_author")
    def test_update_nonexistent_author(self, mock_update_author):
        mock_update_author.return_value = None

        author_id = 1
        author_update = schemas.AuthorUpdate(name="Doesn't matter", id=author_id)

        response = self.client.post(f"/authors/{author_id}", json=author_update.dict())
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
        self.assertEqual(response.headers["content-type"], "text/html; charset=utf-8")
        # assert response.json() == {"detail": "Author not found"}

        mock_update_author.assert_called_once_with(author=author_update)

    @mock.patch("albatross.helpers.database.delete_author")
    def test_delete_author(self, mock_delete_author):
        author_id = 1
        mock_delete_author.return_value = True

        response = self.client.delete(f"/authors/{author_id}")
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.headers["content-type"], "text/html; charset=utf-8")
        # assert response.json()== {"deleted": True}

        mock_delete_author.assert_called_once_with(author_id=author_id)

    @mock.patch("albatross.helpers.database.delete_author")
    def test_delete_nonexistent_author(self, mock_delete_author):
        author_id = 1
        mock_delete_author.return_value = False

        response = self.client.delete(f"/authors/{author_id}")
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
        self.assertEqual(response.headers["content-type"], "text/html; charset=utf-8")
        # assert response.json()== {"detail": "Author not found"}

        mock_delete_author.assert_called_once_with(author_id=author_id)


if __name__ == "__main__":
    import pytest
    pytest.main(["-s", __file__])
