from datetime import datetime, timedelta
from pathlib import Path
import shutil
from unittest.mock import MagicMock, patch

from app import models
from app.main.albatross import article_to_post, compile_posts, create_post


def test_create_post(tmpdir):
    # Create a dictionary with the metadata for the article
    metadata = {"title": "Test article", "author": "Test Author", "slug": "slug"}
    # Create a string with the content for the article
    content = "This is a test article"
    # Call the create_post function and store the result in a variable
    post_file = create_post(content, metadata, tmpdir)

    # Use the assert function to check that the returned path exists and is a file
    assert post_file.exists() and post_file.is_file()
    # Use the assert function to check that the metadata and content of the
    # created article file are correct
    post_content = "---\n"
    post_content += "\n".join([f"{key}: {value}" for key, value in metadata.items()])
    post_content += f"\n---\n\n{content}"

    assert post_file.read_text() == post_content
    Path(metadata["slug"] + ".md").unlink()


def test_create_post_metadata(tmpdir):
    metadata = {
        "title": "My first article",
        "author": "John Smith",
        "created_at": datetime.now(),
        "updated_at": datetime.now() + timedelta(days=2),
        "slug": "test-slug",
        "summary": "A summary of my first article",
        "image_url": "https://example.com/image.jpg",
    }
    content = "This is the content of my first article"

    post_path = create_post(content, metadata, tmpdir)

    post_content = "---\n"
    post_content += "\n".join([f"{key}: {value}" for key, value in metadata.items()])
    post_content += f"\n---\n\n{content}"

    assert post_path.name[-3:] == ".md"
    assert post_content == post_path.read_text()

    Path(metadata["slug"] + ".md").unlink()


def test_article_to_post(session, tmpdir):
    content = "This is the content"
    title = "This is a Title"
    key = "keywords"
    value = "test"
    user = session.get(models.User, 1)
    article_data = models.ArticleData(key=key, value=value)
    article = models.Article(
        title=title,
        content=content,
        user=user
    )
    article.data.append(article_data)
    session.add(article)
    session.commit()

    post_path = article_to_post(article, tmpdir)

    post_content = f"""---
{key}: {value}
author: {article.user.username}
title: {article.title}
date: {article.created_at}
modified: {article.updated_at}
slug: {article.slug}
summary: {article.summary if article.summary else ""}
status: {"draft" if article.is_draft else "published"}
lang: en
translation: False
---

{content}"""
    assert post_path.name[-3:] == ".md"
    assert post_content == post_path.read_text()

    Path(article.slug + ".md").unlink()


def test_article_to_post_with_different_types_of_article_data(session, tmpdir):
    content = "This is the content"
    title = "This is a Title"
    user = session.get(models.User, 1)
    metadata = [
        {"keywords": "test"},
        {"keywords": "pytest"},
        {"tags": "til"},
        {"category": "helpful"}
    ]
    article_data = [
        models.ArticleData(key=key, value=value)
        for data in metadata
        for key, value in data.items()
    ]
    article = models.Article(
        title=title,
        content=content,
        user=user
    )
    article.data = article_data
    article.is_draft = False
    session.add(article)
    session.commit()

    post_path = article_to_post(article, tmpdir)

    post_content = f"""---
keywords: pytest, test
tags: til
category: helpful
author: {article.user.username}
title: {article.title}
date: {article.created_at}
modified: {article.updated_at}
slug: {article.slug}
summary: {article.summary if article.summary else ""}
status: {"draft" if article.is_draft else "published"}
lang: en
translation: False
---

{content}"""

    assert post_path.name[-3:] == ".md"
    assert post_content == post_path.read_text()

    Path(article.slug + ".md").unlink()


def test_compile_posts_compiles_correctly(session):
    user = session.get(models.User, 1)
    articles = [
        models.Article(title=f"Article {i}", content=f"Content {1}", user=user)
        for i in range (5)
    ]

    # make a couple articles not "draft" to ensure proper publishing
    articles[0].is_draft = False
    articles[3].is_draft = False

    for article in articles:
        article.data = [
            models.ArticleData(key="keywords", value=f"test_{i}")
            for i in range(5)
        ]
    session.add_all(articles)
    session.commit()

    compile_posts(articles=articles, directory=None)

    # check that the proper articles were generated
    # - articles marked as "draft" should be in the ./output/drafts directory
    # - articles not marked as "draft" should be in the
    output_dir = Path("./output")
    for article in articles:
        if article.is_draft:
            assert (output_dir / "drafts" / f"{article.slug}.html").exists()
        else:
            assert (output_dir / f"{article.slug}.html").exists()

    # clean up
    shutil.rmtree(Path("output"))


def test_compile_posts_creates_temporary_directory(session):
    user = session.get(models.User, 1)
    articles = [
        models.Article(title=f"Article {i}", content=f"Content {1}", user=user)
        for i in range (5)
    ]

    for article in articles:
        article.data = [
            models.ArticleData(key="keywords", value=f"test_{i}")
            for i in range(5)
        ]
    session.add_all(articles)
    session.commit()

    with patch("app.main.albatross.tempfile.TemporaryDirectory") as mock_temp_dir:
        compile_posts(articles=articles)

    # clean up
    for article in articles:
        post_file = Path(f"{article.slug}.md")
        if post_file.exists():
            post_file.unlink()
    shutil.rmtree(Path("output"))
    assert mock_temp_dir.called_once_with(prefix="content", dir=None)


def test_compile_posts_runs_pelican(session):
    user = session.get(models.User, 1)
    articles = [
        models.Article(title=f"Article {i}", content=f"Content {1}", user=user)
        for i in range (5)
    ]

    for article in articles:
        article.data = [
            models.ArticleData(key="keywords", value=f"test_{i}")
            for i in range(5)
        ]
    session.add_all(articles)
    session.commit()

    with patch("app.main.albatross.pelican") as mock_pelican, \
         patch("app.main.albatross.article_to_post") as mock_article_to_post:
        mock_pelican.Pelican.return_value.run = MagicMock()
        compile_posts(articles=articles, directory=None)


    # clean up
    for article in articles:
        post_file = Path(f"{article.slug}.md")
        if post_file.exists():
            post_file.unlink()

    assert mock_pelican.read_settings.called
    # assert mock_pelican.Pelican.called_once_with(settings=settings)
    assert mock_pelican.Pelican.return_value.run.called


if __name__ == "__main__":
    import pytest
    pytest.main(["-s", __file__])
