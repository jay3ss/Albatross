from flask import url_for

from app import models
from app.jinja.filters import datetime_format


def test_attempt_to_get_all_articles_while_not_authenticated(client):
    response = client.get(url_for("articles.articles"))
    assert response.status_code == 302

    response = client.get(url_for("articles.articles"), follow_redirects=True)
    assert response.status_code == 200
    assert "Sign in" in response.text


def test_attempt_to_get_all_articles_while_authenticated(auth, client, session):
    title = "Test Article Title"
    content = "Test article content"
    user = session.get(models.User, 1)
    article = models.Article(title=title, content=content, user=user)
    session.add(article)
    session.commit()

    auth.login()
    response = client.get(url_for("articles.articles"))

    assert response.status_code == 200
    assert "Articles" in response.text
    assert article.title in response.text
    assert article.slug in response.text


def test_get_single_article_while_authenticated(auth, client, session):
    title = "Test Article Title"
    content = "Test article content"
    user = session.get(models.User, 1)
    article = models.Article(title=title, content=content, user=user)
    session.add(article)
    session.commit()

    auth.login()
    response = client.get(url_for("articles.article", slug=article.slug))

    assert response.status_code == 200
    assert article.title in response.text
    assert article.content in response.text


def test_get_single_article_while_not_authenticated(client, session):
    title = "Test Article Title"
    content = "Test article content"
    user = session.get(models.User, 1)
    article = models.Article(title=title, content=content, user=user)
    session.add(article)
    session.commit()

    response = client.get(
        url_for("articles.article", slug=article.slug), follow_redirects=False
    )

    assert response.status_code == 302
    login_url = url_for("auth.login", _external=False)
    assert response.location[: len(login_url)] == login_url


def test_getting_article_that_does_not_exist(auth, client):
    auth.login()
    response = client.get(
        url_for("articles.article", slug="this-article-does-not-exist"),
        follow_redirects=False,
    )
    assert response.status_code == 404


def test_that_all_articles_are_displayed(app, auth, client, session):
    user = session.get(models.User, 1)
    articles = [
        models.Article(
            title=f"This is Article {i}", content=f"Test Article {i} Content", user=user
        )
        for i in range(app.config["ARTICLES_PER_PAGE"] - 1)
    ]
    session.add_all(articles)

    auth.login()

    response = client.get(url_for("articles.articles"))
    for article in articles:
        assert article.title in response.text
        assert datetime_format(article.created_at) in response.text


def test_get_single_article_while_not_authenticated(client, session):
    title = "Test Article Title"
    content = "Test article content"
    user = session.get(models.User, 1)
    article = models.Article(title=title, content=content, user=user)
    session.add(article)
    session.commit()

    response = client.get(url_for("articles.article", slug=article.slug))
    assert response.status_code == 302

    response = client.get(
        url_for("articles.article", slug=article.slug), follow_redirects=True
    )
    assert response.status_code == 200
    assert "Sign in" in response.text


def test_create_article_while_not_authenticated(client):
    response = client.get(url_for("articles.create_article"), follow_redirects=False)
    assert response.status_code == 302
    login_url = url_for("auth.login", _external=False)
    assert response.location[: len(login_url)] == login_url


def test_create_article_while_authenticated(client, auth):
    auth.login()

    response = client.get(url_for("articles.create_article"))
    assert response.status_code == 200

    response = client.post(
        url_for("articles.create_article"),
        data={
            "title": "Test Article",
            "content": "This is a test article content",
        },
        follow_redirects=True,
    )
    assert response.status_code == 200
    assert "Test Article" in response.text


def test_edit_article_while_authenticated(client, auth, article):
    auth.login()

    response = client.get(url_for("articles.edit_article", slug=article.slug))
    assert response.status_code == 200

    response = client.post(
        url_for("articles.edit_article", slug=article.slug),
        data={
            "title": "Edited Article",
            "content": "This is an edit article content",
        },
        follow_redirects=True,
    )
    assert response.status_code == 200
    assert "Edited Article" in response.text


def test_edit_article_while_not_authenticated(article, client):
    response = client.get(
        url_for("articles.edit_article", slug=article.slug), follow_redirects=False
    )

    assert response.status_code == 302

    # take care of 'next' parameter
    login_url = url_for("auth.login", _external=False)
    assert response.location[: len(login_url)] == login_url

    response = client.get(
        url_for("articles.edit_article", slug=article.slug), follow_redirects=True
    )

    assert response.status_code == 200


def test_edit_nonexistent_article(auth, client):
    auth.login()

    response = client.get(url_for("articles.edit_article", slug="nonexistent"))

    assert response.status_code == 404


def test_delete_article_while_authenticated(client, auth, article, session):
    title = "Test Article Title"
    content = "Test article content"
    user = session.get(models.User, 1)
    article = models.Article(title=title, content=content, user=user)
    session.add(article)
    session.commit()

    articles_before_deletion = models.Article.query.filter_by(user_id=user.id).all()

    auth.login()
    response = client.post(
        url_for("articles.delete_article", slug=article.slug), follow_redirects=False
    )
    articles_after_deletion = models.Article.query.filter_by(user_id=user.id).all()
    assert response.status_code == 302
    assert response.location == url_for("articles.articles", _external=False)
    assert len(articles_before_deletion) - 1 == len(articles_after_deletion)


def test_delete_article_while_not_authenticated(client, article):
    response = client.post(url_for("articles.delete_article", slug=article.slug))

    assert response.status_code == 302
    login_url = url_for("auth.login", _external=False)
    assert response.location[: len(login_url)] == login_url


def test_deleting_article_that_does_not_belong_to_the_user(auth, client, session):
    current_user = session.get(models.User, 1)
    article = models.Article(title="Title", content="Content", user=current_user)
    new_user = models.User(username="bob", email="bob@example.com")
    password = "password"
    new_user.set_password(password)
    session.add(article)
    session.add(new_user)
    session.commit()

    old_article_count = len(models.Article.query.all())

    auth.login(username=new_user.username, password=password)
    client.post(url_for("articles.delete_article", slug=article.slug))
    assert old_article_count == len(models.Article.query.all())


def test_pagination_no_articles(auth, client):
    # Test that no pagination is shown when there are no articles
    auth.login()
    response = client.get(url_for("articles.articles"), follow_redirects=True)
    assert response.status_code == 200
    assert response.request.path == url_for("articles.articles", _external=False)
    assert "No articles found." in response.text
    assert "Next" not in response.text
    assert "Prev" not in response.text


def test_pagination_less_than_articles_per_page(auth, client, session):
    # Set up the Config object with the desired ARTICLES_PER_PAGE value
    # app.config["ARTICLES_PER_PAGE"] = 10

    # Create test data for articles
    username = "fake_user"
    password = "password"
    user = models.User(username=username, email="e@example.com")
    user.set_password(password)
    article = models.Article(title=f"Article 0", content="Content", user=user)

    # Save the test data to the database
    session.add(article)
    session.commit()

    # Test that no pagination is shown when there are less articles than
    # ARTICLES_PER_PAGE
    auth.login(username=username, password=password)
    response = client.get(url_for("articles.articles"))
    assert "Article 0" in response.text
    assert "Next" not in response.text
    assert "Prev" not in response.text


def test_pagination_same_as_articles_per_page(app, auth, client, session):
    # Set up the Config object with the desired ARTICLES_PER_PAGE value
    app.config["ARTICLES_PER_PAGE"] = 10

    # Create test data for articles
    user = session.get(models.User, 1)
    articles = [
        models.Article(title=f"Article {i}", content="Content", user=user)
        for i in range(app.config["ARTICLES_PER_PAGE"])
    ]

    # Save the test data to the database
    session.add_all(articles)
    session.commit()

    # Test that no pagination is shown when there are the same number of articles
    # as ARTICLES_PER_PAGE
    auth.login()
    response = client.get(url_for("articles.articles"))
    assert "Article 0" in response.text
    assert "Article 9" in response.text
    assert "Next" not in response.text
    assert "Prev" not in response.text


def test_pagination_more_than_articles_per_page(app, auth, client, session):
    # Set up the Config object with the desired ARTICLES_PER_PAGE value
    app.config["ARTICLES_PER_PAGE"] = 10

    # Create test data for articles
    user = session.get(models.User, 1)
    articles = [
        models.Article(title=f"Article {i}", content="Content", user=user)
        for i in range(app.config["ARTICLES_PER_PAGE"] + 1)
    ]

    # Save the test data to the database
    session.add_all(articles)
    session.commit()

    # Test that pagination is shown when there are more articles than
    # ARTICLES_PER_PAGE
    auth.login()
    response = client.get(url_for("articles.articles"))
    assert "Article 0" in response.text
    assert "Article 9" in response.text
    assert "Next" in response.text


def test_pagination_pagination_links(app, auth, client, session):
    # Set up the Config object with the desired ARTICLES_PER_PAGE value
    app.config["ARTICLES_PER_PAGE"] = 10

    # Create test data for articles
    user = session.get(models.User, 1)
    articles = [
        models.Article(title=f"Article {i}", content="Content", user=user)
        for i in range(app.config["ARTICLES_PER_PAGE"] * 5)
    ]

    # Save the test data to the database
    session.add_all(articles)
    session.commit()

    auth.login()
    response = client.get(url_for("articles.articles"))
    assert "Article 0" in response.text
    assert "Article 9" in response.text

    response = client.get(url_for("articles.articles", page=2))
    assert "Article 10" in response.text
    assert "Article 14" in response.text

    response = client.get(url_for("articles.articles", page=1))
    assert "Article 0" in response.text
    assert "Article 9" in response.text

    response = client.get(url_for("articles.articles", page=3))
    assert "Article 10" not in response.text
    assert "Article 14" not in response.text

    response = client.get(url_for("articles.articles", page=4))
    assert "Article 10" not in response.text
    assert "Article 14" not in response.text
