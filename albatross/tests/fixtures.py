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
        markdown_path="path/to/post1.md",
        summary="This is a summary of article 1",
    )
    post2 = Article(
        title="Article 2",
        author=author1,
        markdown_path="path/to/post2.md",
        summary="This is a summary of article 2",
    )
    post3 = Article(
        title="Article 3",
        author=author2,
        markdown_path="path/to/post3.md",
        summary="This is a summary of article 3",
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
