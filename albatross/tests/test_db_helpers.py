from albatross.helpers import database as db
from albatross.tests.fixtures import in_memory_prepopulated_db


def test_get_article(in_memory_prepopulated_db):
    temp_db = in_memory_prepopulated_db
