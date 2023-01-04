import pytest
import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker

from albatross.sql_models import Author, Base, Post


@pytest.fixture
def in_memory_db():
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

    post1 = Post(
        title="Post 1",
        author=author1,
        markdown_path="path/to/post1.md",
        summary="This is a summary of post 1",
    )
    post2 = Post(
        title="Post 2",
        author=author1,
        markdown_path="path/to/post2.md",
        summary="This is a summary of post 2",
    )
    post3 = Post(
        title="Post 3",
        author=author2,
        markdown_path="path/to/post3.md",
        summary="This is a summary of post 3",
    )
    session.add(post1)
    session.add(post2)
    session.add(post3)
    session.commit()

    yield session

    # Clean up the database after the tests are done
    session.close()
    engine.dispose()


def test_post_model(in_memory_db):
    # First, let's create a new Post and add it to the session
    author = in_memory_db.query(Author).first()
    new_post = Post(
        title="My First Post",
        author=author,
        markdown_path="/path/to/markdown.md",
        summary="This is a summary of my first post",
    )
    in_memory_db.add(new_post)
    in_memory_db.commit()

    # Now let's retrieve the post from the database and verify that it's the
    # same one we just created
    retrieved_post = in_memory_db.query(Post).all()[-1]
    assert retrieved_post == new_post

    # Let's update the post and commit the changes to the database
    retrieved_post.title = "Updated Title"
    in_memory_db.commit()

    # Now let's retrieve the post again and verify that the changes were saved
    updated_post = in_memory_db.query(Post).all()[-1]
    assert updated_post.title == "Updated Title"

    # Finally, let's delete the post from the database
    in_memory_db.delete(updated_post)
    in_memory_db.commit()

    # Verify that the post was deleted by querying for it and ensuring that it
    # doesn't exist
    assert len(in_memory_db.query(Post).all()) == 3
