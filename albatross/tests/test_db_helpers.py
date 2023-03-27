from albatross.core.models import Author
from albatross.core.schemas import ArticleCreate

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
