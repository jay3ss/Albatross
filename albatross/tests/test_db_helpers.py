from albatross.helpers import database as db
from albatross.tests.fixtures import in_memory_prepopulated_db


def test_get_article(in_memory_prepopulated_db):
    temp_db = in_memory_prepopulated_db
    article = db.get_article_by_id(article_id=1, db=temp_db)
    assert article.id == 1
    assert article.title == "Article 1"
    assert article.author.name == "Author 1"


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