import pytest

from app.models import Article
from tests.fixtures import app, session


# Test generate_slug method
def test_generate_slug():
    title = "Test Article Title"
    slug = Article.generate_slug(title)
    assert isinstance(slug, str)
    assert len(slug) > 0


# Test before_insert event listener for generating slug
def test_generate_slug_before_insert(session):
    title = "Test Article Title"
    article = Article(title=title, content="Test Article Content")
    session.add(article)
    session.commit()
    assert isinstance(article.slug, str)
    assert len(article.slug) > 0
    assert article.slug.startswith(title.lower().replace(" ", "-"))


# Test before_update event listener for generating slug
def test_generate_slug_before_update(session):
    # Create an article
    article = Article(title="Test Article Title", content="Test Article Content")
    session.add(article)
    session.commit()

    # Update the article's title
    new_title = "Updated Article Title"
    article.title = new_title
    session.commit()

    # Check that slug is updated with new title
    assert article.slug.startswith(new_title.lower().replace(" ", "-"))


# Test uniqueness of generated slugs
def test_slug_uniqueness(session):
    title = "Test Article Title"
    articles = [
        Article(title=title, content="Test Article Content")
        for _ in range(20)
    ]
    session.add_all(articles)
    session.commit()

    slugs = set([a.slug for a in articles])
    assert len(slugs) == len(articles)


def test_article_creation(session):
    # Test creating a new Article
    article = Article(
        title="Test Article Title",
        summary="Test Article Summary",
        content="Test Article Content",
        image_url="test.jpg",
        user_id=1
    )
    session.add(article)
    session.commit()
    assert article.id is not None
    assert article.title == "Test Article Title"
    assert article.summary == "Test Article Summary"
    assert article.content == "Test Article Content"
    assert article.image_url == "test.jpg"
    assert article.user_id == 1
    assert article.slug is not None


def test_article_creation_without_optional_fields(session):
    # Test creating a new Article without optional fields
    article = Article(
        title="Test Article Title",
        content="Test Article Content",
    )
    session.add(article)
    session.commit()
    assert article.id is not None
    assert article.title == "Test Article Title"
    assert article.summary is None
    assert article.content == "Test Article Content"
    assert article.image_url is None
    assert article.user_id is None
    assert article.slug is not None


def test_article_creation_with_missing_required_fields(session):
    # Test creating a new Article with missing required fields
    with pytest.raises(Exception):
        article = Article(
            title="Test Article Title",
            summary="Test Article Summary"
            # Missing content field
        )
        session.add(article)
        session.commit()


def test_article_update(session):
    # Test updating an existing Article
    article = Article(
        title="Test Article Title",
        summary="Test Article Summary",
        content="Test Article Content",
        image_url="test.jpg",
        user_id=1
    )
    session.add(article)
    session.commit()

    # Update the Article
    article.title = "Updated Article Title"
    article.summary = "Updated Article Summary"
    article.content = "Updated Article Content"
    article.image_url = "updated.jpg"
    article.user_id = 2
    session.commit()

    # Check that the Article was updated correctly
    updated_article = session.query(Article).filter_by(id=article.id).first()
    assert updated_article.title == "Updated Article Title"
    assert updated_article.summary == "Updated Article Summary"
    assert updated_article.content == "Updated Article Content"
    assert updated_article.image_url == "updated.jpg"
    assert updated_article.user_id == 2


def test_article_deletion(session):
    # Test deleting an Article
    article = Article(
        title="Test Article Title",
        summary="Test Article Summary",
        content="Test Article Content",
        image_url="test.jpg",
        user_id=1
    )
    session.add(article)
    session.commit()

    # Delete the Article
    session.delete(article)
    session.commit()

    # Check that the Article was deleted
    deleted_article = session.query(Article).filter_by(id=article.id).first()
    assert deleted_article is None


def test_article_get_by_id(session):
    # Test getting an Article by its ID
    article = Article(
        title="Test Article Title",
        summary="Test Article Summary",
        content="Test Article Content",
        image_url="test.jpg",
        user_id=1
    )
    session.add(article)
    session.commit()

    # Get the Article by its ID
    retrieved_article = session.get(Article, article.id)

    # Check that the retrieved Article is correct
    assert retrieved_article.id == article.id
    assert retrieved_article.title == "Test Article Title"
    assert retrieved_article


def test_article_string_representation_with_author(session):
    title = "Test Article Title"
    article = Article(
        title=title,
        summary="Test Article Summary",
        content="Test Article Content",
        image_url="test.jpg",
        user_id=1
    )
    session.add(article)
    session.commit()

    user = article.user
    assert title in str(article)
    assert user.username in str(article)


def test_article_string_representation_without_author(session):
    title = "Test Article Title"
    article = Article(
        title=title,
        summary="Test Article Summary",
        content="Test Article Content",
        image_url="test.jpg",
    )
    session.add(article)
    session.commit()

    assert title in str(article)
    assert not "user" in str(article)
