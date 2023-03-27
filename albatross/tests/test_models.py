import pytest
import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker

from albatross.core.models import Author, Base, Article


@pytest.fixture
def in_memory_prepopulated_db():
    engine = sa.create_engine("sqlite:///:memory:")
    Session = sessionmaker(bind=engine)
    session = Session()

    # Create the database tables
    Base.metadata.create_all(bind=engine)

    # Pre-populate the database with some test data
    author1 = Author(name="Author 1")
    author2 = Author(name="Author 2")
    session.add(author1)
    session.add(author2)
    session.commit()

    post1 = Article(
        title="Article 1",
        author=author1,
        content="This is a content of article 1",
    )
    post2 = Article(
        title="Article 2",
        author=author1,
        content="This is a content of article 2",
    )
    post3 = Article(
        title="Article 3",
        author=author2,
        content="This is a content of article 3",
    )
    session.add(post1)
    session.add(post2)
    session.add(post3)
    session.commit()

    yield session

    # Clean up the database after the tests are done
    session.close()
    engine.dispose()


@pytest.fixture
def in_memory_db():
    engine = sa.create_engine("sqlite:///:memory:")
    Session = sessionmaker(bind=engine)
    session = Session()

    # Create the database tables
    Base.metadata.create_all(bind=engine)

    yield session

    # Clean up the database after the tests are done
    session.close()
    engine.dispose()


def test_author_model(in_memory_db):
    # Create a new author
    author = Author(name="John Smith")

    # Add the author to the session
    in_memory_db.add(author)

    # Commit the session to write the author to the database
    in_memory_db.commit()

    # Query the author from the database
    retrieved_author = in_memory_db.query(Author).first()

    # Assert that the retrieved author has the same name as the one we created
    assert retrieved_author.name == "John Smith"


def test_post_model(in_memory_db):
    # First, let's create a new Article and add it to the session
    author = Author(name="Author 1")
    new_post = Article(
        title="My First Article",
        author=author,
        content="This is a content of my first article",
    )
    in_memory_db.add(new_post)
    in_memory_db.commit()

    # Now let's retrieve the article from the database and verify that it's the
    # same one we just created
    retrieved_post = in_memory_db.query(Article).first()
    assert retrieved_post == new_post

    # Let's update the article and commit the changes to the database
    retrieved_post.title = "Updated Title"
    in_memory_db.commit()

    # Now let's retrieve the article again and verify that the changes were saved
    updated_post = in_memory_db.query(Article).first()
    assert updated_post.title == "Updated Title"

    # Finally, let's delete the article from the database
    in_memory_db.delete(updated_post)
    in_memory_db.commit()

    # Verify that the article was deleted by querying for it and ensuring that it
    # doesn't exist
    deleted_post = in_memory_db.query(Article).first()
    assert deleted_post is None


def test_author_model_with_prepopulated_data(in_memory_prepopulated_db):
    # Get a session from the in_memory_db fixture
    session = in_memory_prepopulated_db

    # Query the authors from the prepopulated data
    authors = session.query(Author).all()
    assert len(authors) == 2

    # Verify that the first author's name is correct
    first_author = authors[0]
    assert first_author.name == "Author 1"

    # Verify that the first author has 2 articles
    assert len(first_author.articles) == 2

    # Verify that the second author's name is correct
    second_author = authors[1]
    assert second_author.name == "Author 2"

    # Verify that the second author has 1 articles
    assert len(second_author.articles) == 1
