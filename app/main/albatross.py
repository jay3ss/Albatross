from pathlib import Path
from tempfile import NamedTemporaryFile

from app.models import Article


def create_post(content: str, metadata: list[dict], base_dir: Path) -> Path:
    """
    Create a new (temporary) article file with the given metadata and content.

    Parameters:
        content (str): The content of the article.
        metadata (list[dict]): The metadata for the article.
        base_dir (Path): The base directory where the article file will be created.

    Returns:
        Path: path to the temporary article file
    """
    tf = NamedTemporaryFile(dir=base_dir, suffix=".md", mode="w", delete=False)

    tf.write("---\n")
    for key, value in metadata.items():
        tf.write(f"{key}: {value}\n")
    tf.write("---\n")
    tf.write("\n" + content)
    file_path = Path(tf.name)
    tf.close()

    return file_path


def article_to_post(article: Article) -> Path:
    metadata = [ad.to_dict() for ad in article.data]
    return create_post(article.content)
