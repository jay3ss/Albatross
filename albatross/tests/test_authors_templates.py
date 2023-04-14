# from albatross.core import forms, models
# from albatross.helpers import database as db
# from albatross.helpers import templates as th
# from albatross.tests.fixtures import in_memory_prepopulated_db, templates_env, test_app


# def test_authors_index_template(templates_env, test_app):
#     template = templates_env.get_template("authors/index.html")

#     authors = [models.Author(name="Author 1", id=1), models.Author(name="Author 2", id=2)]
#     app = test_app
#     url_for = app.url_path_for
#     rendered = template.render(authors=authors, url_for=url_for)

#     assert "<title>Authors</title>" in rendered
#     for author in authors:
#         assert author.name in rendered
#         assert f"href=\"/authors/{author.id}\"" in rendered
#         assert f"<em>{len(author.articles)} articles</em>"


# def test_show_author_template(templates_env):
#     template = templates_env.get_template("authors/show.html")

#     author = models.Author(name="Author 1")
#     app = test_app
#     url_for = app.url_path_for
#     rendered = template.render(author=author, url_for=url_for)

#     assert f"<title>{author.name}</title>" in rendered
#     assert f"<h1>{author.name}</h1>" in rendered
#     assert f"{author.name} has <em>0 articles</em>" in rendered
#     assert "<a href=\"/authors/\">Back</a>" in rendered


# def test_show_author_template_with_articles(in_memory_prepopulated_db, templates_env):
#     temp_db = in_memory_prepopulated_db
#     template = templates_env.get_template("authors/show.html")

#     author = db.get_author_by_id(author_id=1, db=temp_db)
#     app = test_app
#     url_for = app.url_path_for
#     rendered = template.render(author=author, url_for=url_for)

#     assert f"<title>{author.name}</title>" in rendered
#     assert f"<h1>{author.name}</h1>" in rendered
#     assert f"{author.name} has <em>{len(author.articles)} articles</em>" in rendered
#     for article in author.articles:
#         assert article.title in rendered
#         assert f"<em>on {th.datetime_format(article.created_at)}</em>" in rendered
#     assert "<a href=\"/authors/\">Back</a>" in rendered


# def test_new_author_template_with_empty_form(templates_env):
#     template = templates_env.get_template("authors/new.html")

#     form = forms.NewAuthorForm()
#     app = test_app
#     url_for = app.url_path_for
#     rendered = template.render(form=form, url_for=url_for)

#     assert "<title>New Author</title>" in rendered
#     assert "Create Author" in rendered
#     assert "<form" in rendered
#     assert "action=\"/authors/new\"" in rendered
#     assert "method=\"post\"" in rendered
#     assert "<label" in rendered
#     assert "for=\"name\"" in rendered
#     assert "<label" in rendered
#     assert "name=\"name\"" in rendered
#     assert "type=\"text\"" in rendered
#     assert "<button" in rendered
#     assert ">Submit<" in rendered


# if __name__ == "__main__":
#     import pytest
#     pytest.main(["-s", __file__])
