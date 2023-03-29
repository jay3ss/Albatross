from http import HTTPStatus
from unittest import mock

from fastapi.testclient import TestClient

from albatross.core import models
from albatross.core import schemas
from albatross.main import app


app.debug = True
client = TestClient(app)


@mock.patch("albatross.helpers.database.get_author_by_id")
def test_get_existing_author(mock_get_author):
    mock_author = schemas.Author(id=1, name="John Doe")
    mock_get_author.return_value = mock_author

    response = client.get("/authors/1")
    assert response.status_code == HTTPStatus.OK
    assert response.json()["author"] == mock_author.dict()

    mock_get_author.assert_called_once_with(author_id=1)


@mock.patch("albatross.helpers.database.get_author_by_id")
def test_get_nonexistent_author(mock_get_author):
    mock_author = None
    mock_get_author.return_value = mock_author
    author_id = 1

    response = client.get(f"/authors/{author_id}")
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {"detail": "Author not found"}

    mock_get_author.assert_called_once_with(author_id=author_id)


@mock.patch("albatross.helpers.database.get_authors")
def test_get_all_authors_no_limit(mock_get_authors):
    mock_authors = [models.Author(name=f"Author {i}") for i in range(10)]
    mock_get_authors.return_value = mock_authors

    response = client.get("/authors")
    assert response.status_code == HTTPStatus.OK
    assert len(response.json()) == len(mock_authors)

    mock_get_authors.assert_called_once_with(limit=None)


@mock.patch("albatross.helpers.database.get_authors")
def test_get_all_authors_limit_5(mock_get_authors):
    mock_authors = [models.Author(name=f"Author {i}") for i in range(5)]
    mock_get_authors.return_value = mock_authors

    response = client.get("/authors", params={"limit": 5})
    assert response.status_code == HTTPStatus.OK
    assert len(response.json()) == len(mock_authors)

    mock_get_authors.assert_called_once_with(limit=5)


@mock.patch("albatross.helpers.database.create_author")
def test_create_author(mock_create_author):
    mock_author = models.Author(name="Jane Doe", id=1)
    mock_create_author.return_value = mock_author
    new_author = schemas.Author(name=mock_author.name, id=mock_author.id)

    response = client.post("/authors/new", json=new_author.dict())
    assert response.status_code == HTTPStatus.CREATED
    assert response.json()["name"] == new_author.name
    assert response.json()["id"] == mock_author.id

    mock_create_author.assert_called_once_with(
        schemas.AuthorCreate(name="Jane Doe")
    )


@mock.patch("albatross.helpers.database.update_author")
def test_update_author(mock_update_author):
    author_id = 1
    new_name = "New Name"
    mock_updated_author = models.Author(name=new_name, id=author_id)
    mock_update_author.return_value = mock_updated_author

    author_update = schemas.AuthorUpdate(name=new_name, id=author_id)

    response = client.put(f"/authors/{author_id}", json=author_update.dict())
    assert response.status_code == HTTPStatus.OK
    assert response.json()["author"] == {"name": new_name, "id": author_id}

    mock_update_author.assert_called_once_with(author=author_update)


@mock.patch("albatross.helpers.database.update_author")
def test_update_nonexistent_author(mock_update_author):
    mock_update_author.return_value = None

    author_id = 1
    author_update = schemas.AuthorUpdate(name="Doesn't matter", id=author_id)

    response = client.put(f"/authors/{author_id}", json=author_update.dict())
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {"detail": "Author not found"}

    mock_update_author.assert_called_once_with(author=author_update)


@mock.patch("albatross.helpers.database.delete_author")
def test_delete_author(mock_delete_author):
    author_id = 1
    mock_delete_author.return_value = True

    response = client.delete(f"/authors/{author_id}")
    assert response.status_code == HTTPStatus.OK
    assert response.json()== {"deleted": True}

    mock_delete_author.assert_called_once_with(author_id=author_id)


@mock.patch("albatross.helpers.database.delete_author")
def test_delete_nonexistent_author(mock_delete_author):
    author_id = 1
    mock_delete_author.return_value = False

    response = client.delete(f"/authors/{author_id}")
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json()== {"detail": "Author not found"}

    mock_delete_author.assert_called_once_with(author_id=author_id)


if __name__ == "__main__":
    import pytest
    pytest.main(["-s", __file__])
