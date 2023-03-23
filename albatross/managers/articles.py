from pathlib import Path
from tempfile import NamedTemporaryFile


def create_post(metadata: dict, content: str, base_dir: Path) -> Path:
    """
    Create a new (temporary) post file with the given metadata and content.

    Parameters:
        metadata (dict): The metadata for the post.
        content (str): The content of the post.
        base_dir (Path): The base directory where the post file will be created.

    Returns:
        Path: path to the temporary post file
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
