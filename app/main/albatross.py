import os
from pathlib import Path
import tempfile

import pelican

from app.models import Article


def compile_posts(articles: list[Article], directory: Path | None = None) -> Path:
    """
    Compile a list of Article objects into Pelican-ready Markdown files in a
    temporary directory.

    Args:
        articles (list[Article]): A list of Article objects to be compiled.
        directory (Path | None, optional): The directory where the temporary
        directory will be created. Defaults to None.
    """
    settings = pelican.read_settings()
    with tempfile.TemporaryDirectory(prefix="content", dir=directory) as td:
        for article in articles:
            article_to_post(article=article, base_dir=td)

        settings["PATH"] = td
        pel = pelican.Pelican(settings=settings)
        pel.run()


def create_post(content: str, metadata: dict, base_dir: Path) -> Path:
    """
    Create a new (temporary) article file with the given metadata and content.

    Args:
        content (str): The content of the article.
        metadata (dict): The metadata for the article.
        base_dir (Path): The base directory where the article file will be created.

    Returns:
        Path: path to the temporary article file
    """
    temp_fd, temp_path = tempfile.mkstemp(
        suffix=".md",
        prefix="albatross-",
        dir=base_dir,
    )
    text = "---\n"
    for key, value in metadata.items():
        # metadata can be a list (set here) or a string, integer, ...
        if isinstance(value, set):
            text += f"{key}: {', '.join(sorted([v for v in value]))}\n"
        else:
            text += f"{key}: {value}\n"
    text += "---\n\n" + content

    with os.fdopen(temp_fd, "w+") as tf:
        tf.write(text)
    # a Markdown post for Pelican has the following format:
    # ---
    # metadata_key_1: metadata_value_1
    # metadata_key_2: metadata_value_2
    # ...
    # metadata_key_n: metadata_value_n
    # ---
    # content
    file_path = Path(temp_path)

    return file_path


def article_to_post(article: Article, base_dir: Path) -> Path:
    """
    Convert an Article object to a Pelican-ready markdown post.

    Args:
        article (Article): The article to convert.
        base_dir (Path): The base directory where the post file will be created.

    Returns:
        Path: The path to the Pelican-ready markdown post file.
    """
    metadata = _create_metadata(article)
    return create_post(article.content, metadata, base_dir)


def _create_metadata(article: Article) -> dict:
    """
    Create a dictionary of metadata for a Pelican-ready markdown post.

    Args:
        article (Article): The article to create metadata for.

    Returns:
        dict: The metadata dictionary.

    Metadata info found at:
    https://docs.getpelican.com/en/stable/content.html#file-metadata
    """
    metadata_lists = ["tags", "keywords"]
    metadata = {}
    for data in article.data:
        if data.key in metadata_lists:
            if not data.key in metadata:
                metadata[data.key] = set([data.value])
            else:
                metadata[data.key].add(data.value)
        else:
            metadata[data.key] = data.value

    metadata.update({
        "author": article.user.username,
        "title": article.title,
        "date": article.created_at,
        "modified": article.updated_at,
        "slug": article.slug,
        "summary": article.summary if article.summary else "",
        "status": "draft" if article.is_draft else "published",
        "lang": "en",
        "translation": False,
    })
    return metadata
