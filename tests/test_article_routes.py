from flask import url_for


def test_attempt_to_get_all_articles_while_not_authenticated(client):
    response = client.get(url_for("articles.articles"))
    assert response.status_code == 302

    response = client.get(url_for("articles.articles"), follow_redirects=True)
    assert response.status_code == 200
    assert "Sign in" in response.text


def test_attempt_to_get_all_articles_while_authenticated(auth, client):
    auth.login()
    response = client.get(url_for("articles.articles"))
    assert response.status_code == 200
    assert "Articles" in response.text


def test_create_article(client, auth):
    auth.login()
    response = client.post(
        url_for("articles.create_article"),
        data={
            "title": "Test Article",
            "content": "This is a test article content"
        },
        follow_redirects=True
    )
    assert response.status_code == 200
    assert "Test Article" in response.text


def test_get_article(client, article):
    response = client.get(url_for("articles.article", slug=article.slug))
    assert response.status_code == 200
    assert article.title in response.text


def test_update_article(client, auth, article):
    auth.login()
    response = client.post(
        url_for("articles.update_article", slug=article.slug),
        data={
            "title": "Updated Article",
            "content": "This is an updated article content",
        },
        follow_redirects=True
    )
    assert response.status_code == 200
    assert "Updated Article" in response.text


def test_delete_article(client, auth, article):
    auth.login()
    response = client.post(
        url_for("articles.delete_article", slug=article.slug),
        follow_redirects=True
    )
    assert response.status_code == 200
    assert "Article deleted" in response.text

