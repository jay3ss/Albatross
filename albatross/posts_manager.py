from pathlib import Path


def create_post(metadata: dict, content: str, base_dir: Path) -> Path:
    """
    Create a new post file with the given metadata and content.

    Parameters:
        metadata: A dictionary containing the metadata for the post.
        content: The content of the post, as a string.
        base_dir: The base directory where the post file should be created.

    Returns:
        The path to the created post file.
    """
    # Create the filename for the post, using the metadata
    filename = f"{metadata['date']}-{metadata['slug']}.md"

    # Create the full path for the post file
    file_path = base_dir / "content" / "posts" / filename

    # Open the post file in write mode
    with file_path.open("w") as f:
        # Write the metadata to the file
        for key, value in metadata.items():
            f.write(f"{key}: {value}\n")

        # Write the content to the file
        f.write("\n" + content)

    # Return the path to the created post file
    return file_path
