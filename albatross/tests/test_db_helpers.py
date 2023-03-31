"""TODO: write tests for every logical branch in the functions"""
from albatross.core.models import Author
from albatross.core.schemas import ArticleCreate, ArticleUpdate, AuthorCreate, AuthorUpdate

from albatross.helpers import database as db
from albatross.tests.fixtures import in_memory_db, in_memory_prepopulated_db


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
    author_id = 1
    # article = db.get_article_by_id(article_id=author_id, db=temp_db)
    db.delete_article(article_id=author_id, db=temp_db)
    articles = db.get_articles(db=temp_db)
    assert len(articles) == 2
    assert articles[0].id == 2
    assert articles[1].id == 3
    assert db.get_article_by_id(article_id=author_id, db=temp_db) == None


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


def test_create_author(in_memory_db):
    temp_db = in_memory_db
    authors = db.get_authors(db=temp_db)
    new_author= AuthorCreate(name="Author 1")
    db.create_author(author=new_author, db=temp_db)
    authors_again = db.get_authors(db=temp_db)
    assert len(authors_again) == len(authors) + 1


def test_update_author_name(in_memory_prepopulated_db):
    temp_db = in_memory_prepopulated_db
    author_id = 1
    author = db.get_author_by_id(author_id=author_id, db=temp_db)
    new_name = "My New Name"
    updated_author = db.update_author(AuthorUpdate(name=new_name, id=author.id), db=temp_db)
    assert updated_author.name == new_name
    assert updated_author.id == author_id


def test_deleting_author(in_memory_prepopulated_db):
    temp_db = in_memory_prepopulated_db
    author_id = 1
    authors = db.get_authors(db=temp_db)
    was_deleted = db.delete_author(author_id=author_id, db=temp_db)
    authors_again = db.get_authors(db=temp_db)
    assert was_deleted
    assert len(authors) -1 == len(authors_again)


def test_attempting_to_delete_author_that_dne(in_memory_prepopulated_db):
    temp_db = in_memory_prepopulated_db
    author_id = 1000000
    authors = db.get_authors(db=temp_db)
    was_deleted = db.delete_author(author_id=author_id, db=temp_db)
    authors_again = db.get_authors(db=temp_db)
    assert not was_deleted
    assert len(authors) == len(authors_again)


def test_get_authors(in_memory_prepopulated_db):
    temp_db = in_memory_prepopulated_db
    authors = db.get_authors(db=temp_db)
    assert len(authors) == 2


def test_get_authors_limited_less_than_exist(in_memory_prepopulated_db):
    temp_db = in_memory_prepopulated_db
    limit = 1
    authors = db.get_authors(limit=limit, db=temp_db)
    assert len(authors) == limit


def test_get_authors_limited_more_than_exist(in_memory_prepopulated_db):
    temp_db = in_memory_prepopulated_db
    limit = 1000
    authors = db.get_authors(limit=limit, db=temp_db)
    assert len(authors) == 2
