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


if __name__ == "__main__":
    import pytest
    pytest.main(["-s", __file__])
