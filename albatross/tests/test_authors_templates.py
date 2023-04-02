import jinja2

from albatross.core import models
from albatross.main import app


def test_authors_index_template():
    template = jinja2.Environment(
        loader=jinja2.PackageLoader("albatross", "templates")
    ).get_template("authors/index.html")

    authors = [models.Author(name="Author 1"), models.Author(name="Author 2")]
    url_for = app.url_path_for
    rendered = template.render(authors=authors, url_for=url_for)

    assert "<title>Authors</title>" in rendered
    assert "Author 1 <em>0 articles</em>"
    assert "Author 2 <em>0 articles</em>"


def test_show_author_template():
    template = jinja2.Environment(
        loader=jinja2.PackageLoader("albatross", "templates")
    ).get_template("authors/show.html")

    author = models.Author(name="Author 1")
    url_for = app.url_path_for
    rendered = template.render(author=author, url_for=url_for)

    assert f"<title>{author.name}</title>" in rendered
    assert f"<h1>{author.name}</h1>"
    assert f"{author.name} has <em>0 articles</em>"


if __name__ == "__main__":
    import pytest
    pytest.main(["-s", __file__])
