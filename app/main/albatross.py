import os
from pathlib import Path
import shutil
import tempfile

import pelican

from app.jinja.filters import datetime_format
from app.models import Article


def compile_posts(
    articles: list[Article], directory: Path = None, cleanup: bool = True
) -> Path:
    """
    Compile a list of Article objects into Pelican-ready Markdown files and
    compiles the site into an archive. Returns the output as an archive
    (`{username}-output.zip`).

    Args:
        articles (list[Article]): A list of Article objects to be compiled.
        directory (Path, optional): The directory where the temporary directory
        will be created. Defaults to None.
        cleanup (bool, optional): Clean up output directory. NOTE: This does NOT
        remove the archived output. Defaults to True.

    Returns:
        The path to the archive of the compiled site.
    """
    # TODO: this will need to be the user settings once properly implemented
    settings = pelican.read_settings()
    with tempfile.TemporaryDirectory(prefix="content", dir=directory) as td:
        for article in articles:
            article_to_post(article=article, base_dir=td)

        settings["PATH"] = td
        settings["ARTICLE_PATHS"] = td
        output_path = _output_path(articles[0])
        settings["OUTPUT_PATH"] = output_path
        pel = pelican.Pelican(settings=settings)
        pel.run()

    zip_path = shutil.make_archive(output_path, "zip", output_path)
    if cleanup:
        shutil.rmtree(output_path)
    return zip_path


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

    # TODO: this will need to be the user settings once properly implemented
    settings = pelican.read_settings()
    # TODO:
    # - make this date format the default setting and allow the user to update this
    # - set the modified date as the same above, but only if it's not `None`
    # date_format_str = "%Y/%m/%d %I:%M%p"
    date_format_str = settings["DEFAULT_DATE_FORMAT"]
    metadata.update(
        {
            "author": article.user.username,
            "title": article.title,
            "date": datetime_format(article.created_at, date_format_str),
            # "modified": datetime_format(article.updated_at, date_format_str),
            "slug": article.slug,
            "summary": article.summary if article.summary else "",
            "status": "draft" if article.is_draft else "published",
            "lang": "en",
            "translation": False,
        }
    )
    return metadata


def _output_path(article: Article, *args) -> Path:
    """Returns the output path for Pelican

    Args:
        article (Article): the article to get the username from

    Returns:
        Path: the output path
    """
    parts = [article.user.username_lower]
    parts.extend(args)
    parts.extend(["output"])
    # return Path("-".join(parts))

    temp_path = tempfile.mkdtemp(suffix="-".join(parts))
    return temp_path
