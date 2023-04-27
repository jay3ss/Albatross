from datetime import datetime, timedelta

from app.main.albatross import create_post, article_to_post
from app import models


def test_create_post(tmpdir):
    # Create a dictionary with the metadata for the article
    metadata = {"title": "Test article", "author": "Test Author"}
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
