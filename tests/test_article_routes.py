from flask import url_for

from app import models


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

    response = client.get(url_for("articles.article", slug=article.slug))
    assert response.status_code == 302

    response = client.get(
        url_for("articles.article", slug=article.slug),
        follow_redirects=True
    )
    assert response.status_code == 200
    assert "Sign in" in response.text


def test_create_article(client, auth):
    auth.login()
    response = client.post(
        url_for("articles.create_article"),
        data={
            "title": "Test Article",
            "content": "This is a test article content",
            # "summary": "",
        },
        follow_redirects=True
    )
    assert response.status_code == 200
    assert "Test Article" in response.text


def test_edit_article_while_authenticated(client, auth, article):
    auth.login()
    response = client.post(
        url_for("articles.edit_article", slug=article.slug),
        data={
            "title": "Edited Article",
            "content": "This is an edit article content",
        },
        follow_redirects=True
    )
    assert response.status_code == 200
    assert "Edited Article" in response.text


def test_delete_article(client, auth, article):
    auth.login()
    response = client.post(
        url_for("articles.delete_article", slug=article.slug),
        follow_redirects=True
    )
    assert response.status_code == 200
    assert "Article deleted" in response.text

