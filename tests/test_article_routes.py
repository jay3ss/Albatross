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


def test_that_all_articles_are_displayed(auth, client, session):
    user = session.get(models.User, 1)
    articles = [
        models.Article(
            title=f"This is Article {i}",
            content=f"Test Article {i} Content",
            user=user
        )
        for i in range(20)
    ]
    session.add_all(articles)

    auth.login()

    response = client.get(url_for("articles.articles"))
    for article in articles:
        assert article.title in response.text
        assert article.created_at.strftime('%Y-%m-%d') in response.text


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


def test_edit_article_while_not_authenticated(article, client):
    response = client.get(
        url_for("articles.edit_article", slug=article.slug),
        follow_redirects=False
    )

    assert response.status_code == 302

    # take care of 'next' parameter
    login_url = url_for("auth.login", _external=False)
    assert response.location[:len(login_url)] == login_url

    response = client.get(
        url_for("articles.edit_article", slug=article.slug),
        follow_redirects=True
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
        url_for("articles.delete_article", slug=article.slug),
        follow_redirects=False
    )
    articles_after_deletion = models.Article.query.filter_by(user_id=user.id).all()
    assert response.status_code == 302
    assert response.location == url_for("articles.articles", _external=False)
    assert len(articles_before_deletion) - 1 == len(articles_after_deletion)



def test_delete_article_while_not_authenticated(client, article):
    response = client.post(
        url_for("articles.delete_article", slug=article.slug)
    )

    assert response.status_code == 302
    login_url = url_for("auth.login", _external=False)
    assert response.location[:len(login_url)] == login_url
