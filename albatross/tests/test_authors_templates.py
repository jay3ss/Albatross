from albatross.core import models


def test_authors_index_template():
    template = jinja2.Environment(
        loader=jinja2.PackageLoader("albatross", "templates")
    ).get_template("authors/index.html")

    authors = [models.Author(name="Author 1"), models.Author(name="Author 2")]
    rendered = template.render(context={"authors": authors})

    assert "<title>Authors</title>" in rendered
    assert "Author 1 <em>0 articles</em>"
    assert "Author 2 <em>0 articles</em>"
