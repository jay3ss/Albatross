import uuid

from slugify import slugify


def generate_slug(text: str) -> str:
    """
    Generates a slug based on the given article title, using a combination of the
    title, a part of a UUID, and slugification.

    Args:
        text (str): The text to be slugified.

    Returns:
        str: The generated slug.
    """
    uuid_part = str(uuid.uuid4())[:8]
    url = f"{slugify(text)}-{uuid_part}"
    return url
