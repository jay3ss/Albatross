from albatross.core.models import Author
from albatross.core.schemas import ArticleCreate, ArticleUpdate

from albatross.helpers import database as db
from albatross.tests.fixtures import in_memory_prepopulated_db


def test_get_article_by_id(in_memory_prepopulated_db):
    temp_db = in_memory_prepopulated_db
    article = db.get_article_by_id(article_id=1, db=temp_db)
    assert article.id == 1
    assert article.title == "Article 1"
    assert article.author.name == "Author 1"


def test_get_article_by_id_that_does_not_exist(in_memory_prepopulated_db):
    temp_db = temp_db = in_memory_prepopulated_db
    article = db.get_article_by_id(article_id=1000, db=temp_db)
    assert article == None


def test_get_articles(in_memory_prepopulated_db):
    temp_db = in_memory_prepopulated_db
    articles = db.get_articles(db=temp_db)
    assert len(articles) == 3
    for i, article in enumerate(articles, start=1):
        assert article.title == f"Article {i}"


def test_get_articles_limited_to_less_than_total_num_of_articles(in_memory_prepopulated_db):
    temp_db = in_memory_prepopulated_db
    articles = db.get_articles(limit=2, db=temp_db)
    assert len(articles) == 2
    for i, article in enumerate(articles, start=1):
        assert article.title == f"Article {i}"


def test_get_articles_limited_to_same_num_of_articles(in_memory_prepopulated_db):
    temp_db = in_memory_prepopulated_db
    articles = db.get_articles(limit=3, db=temp_db)
    assert len(articles) == 3
    for i, article in enumerate(articles, start=1):
        assert article.title == f"Article {i}"


def test_get_articles_limited_to_more_than_total_num_of_articles(in_memory_prepopulated_db):
    temp_db = in_memory_prepopulated_db
    articles = db.get_articles(limit=4, db=temp_db)
    assert len(articles) == 3
    for i, article in enumerate(articles, start=1):
        assert article.title == f"Article {i}"


def test_delete_article(in_memory_prepopulated_db):
    temp_db = in_memory_prepopulated_db
    db.delete_article(article_id=1, db=temp_db)
    articles = db.get_articles(db=temp_db)
    assert len(articles) == 2
    assert articles[0].id == 2
    assert articles[1].id == 3
    assert db.get_article_by_id(article_id=1, db=temp_db) == None


def test_create_article(in_memory_prepopulated_db):
    temp_db = in_memory_prepopulated_db
    articles = db.get_articles(db=temp_db)
    author = temp_db.query(Author).first()
    new_article = ArticleCreate(
        title="New Article",
        content="This is an article",
        author_id=author.id
    )
    db.create_article(article=new_article, db=temp_db)
    articles_again = db.get_articles(db=temp_db)
    assert len(articles_again) == len(articles) + 1


def test_update_article_title(in_memory_prepopulated_db):
    temp_db = in_memory_prepopulated_db
    article = db.get_article_by_id(article_id=1, db=temp_db)
    new_title = "I've just changed the title".title()
    new_article = ArticleUpdate(
        title=new_title,
        author_id=article.author_id,
        content=article.content,
        id=article.id
    )
    db.update_article(article=new_article, db=temp_db)
    updated_article = db.get_article_by_id(article_id=article.id, db=temp_db)
    assert updated_article.title == new_title
    assert updated_article.content == article.content
    assert updated_article.author_id == article.author_id
    assert updated_article.id == article.id


def test_update_article_content(in_memory_prepopulated_db):
    temp_db = in_memory_prepopulated_db
    article = db.get_article_by_id(article_id=1, db=temp_db)
    new_content = "I've just changed the content of the article"
    new_article = ArticleUpdate(
        title=article.title,
        author_id=article.author_id,
        content=new_content,
        id=article.id
    )
    db.update_article(article=new_article, db=temp_db)
    updated_article = db.get_article_by_id(article_id=article.id, db=temp_db)
    assert updated_article.title == article.title
    assert updated_article.content == new_content
    assert updated_article.author_id == article.author_id
    assert updated_article.id == article.id


def test_update_article_author(in_memory_prepopulated_db):
    temp_db = in_memory_prepopulated_db
    article = db.get_article_by_id(article_id=1, db=temp_db)
    new_author_id = 2
    new_article = ArticleUpdate(
        title=article.title,
        author_id=new_author_id,
        content=article.content,
        id=article.id
    )
    db.update_article(article=new_article, db=temp_db)
    updated_article = db.get_article_by_id(article_id=article.id, db=temp_db)
    assert updated_article.title == article.title
    assert updated_article.content == article.content
    assert updated_article.author_id == new_author_id
    assert updated_article.id == article.id


def test_get_author_by_id(in_memory_prepopulated_db):
    temp_db = in_memory_prepopulated_db
    author = db.get_author_by_id(author_id=1, db=temp_db)
    assert author.id == 1
    assert author.name == "Author 1"


if __name__ == "__main__":
    import pytest
    pytest.main(["-s", __file__])
