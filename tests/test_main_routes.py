from flask import url_for


def test_getting_main_page_while_not_authenticated(client):
    response = client.get(
        url_for("main.index"),
        follow_redirects=False
    )
    assert response.status_code == 200
