from pathlib import Path
from tempfile import NamedTemporaryFile, TemporaryFile


def create_post(metadata: dict, content: str, base_dir: Path) -> Path:
    """
    Create a new (temporary) post file with the given metadata and content.

    Parameters:
        metadata: A dictionary containing the metadata for the post.
        content: The content of the post, as a string.
        base_dir: The base directory where the post file should be created.

    Returns:
        The path to the temporary post file
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
