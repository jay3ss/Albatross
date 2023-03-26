from albatross.helpers import database as db
from albatross.tests.fixtures import in_memory_prepopulated_db


def test_get_article(in_memory_prepopulated_db):
    temp_db = in_memory_prepopulated_db
    article = db.get_article_by_id(article_id=1, db=temp_db)
    assert article.id == 1
    assert article.title == "Article 1"
    assert article.author.name == "Author 1"
