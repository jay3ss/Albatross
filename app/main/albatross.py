from pathlib import Path
from tempfile import NamedTemporaryFile

from app.models import Article


def create_post(content: str, metadata: dict, base_dir: Path) -> Path:
    """
    Create a new (temporary) article file with the given metadata and content.

    Parameters:
        content (str): The content of the article.
        metadata (dict): The metadata for the article.
        base_dir (Path): The base directory where the article file will be created.

    Returns:
        Path: path to the temporary article file
    """
    tf = NamedTemporaryFile(dir=base_dir, suffix=".md", mode="w", delete=False)

    tf.write("---\n")
    for key, value in metadata.items():
        if isinstance(value, set):
            tf.write(f"{key}: {', '.join(sorted([v for v in value]))}\n")
        else:
            tf.write(f"{key}: {value}\n")
    tf.write("---\n")
    tf.write("\n" + content)
    file_path = Path(tf.name)
    tf.close()

    return file_path


def article_to_post(article: Article, base_dir: Path) -> Path:
    """
    _summary_

    Args:
        article (Article): _description_
        base_dir (Path): _description_

    Returns:
        Path: _description_
    """
    metadata = _create_metadata(article)
    return create_post(article.content, metadata, base_dir)


def _create_metadata(article: Article) -> dict:
    """
    _summary_

    Args:
        article (Article): _description_

    Returns:
        dict: _description_

    metadata info found at:
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
