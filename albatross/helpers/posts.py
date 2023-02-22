import re


def generate_introduction(post_contents: str, max_length: int = 150) -> str:
    """Generate a brief introduction to a post based on its contents.

    Args:
        post_contents: The contents of the post.
        max_length: The maximum length of the introduction.

    Returns:
        A brief introduction to the post.
    """
    # Split the post contents into a list of sentences
    sentences = re.split(r"(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?|\n)\s", post_contents)

    # Find the first sentence that is less than or equal to the maximum length
    introduction = ""
    for sentence in sentences:
        if len(sentence) <= max_length:
            introduction = sentence
            break

    # If no suitable sentence was found, use the first sentence
    if not introduction:
        introduction = sentences[0]

    # Trim the introduction to the maximum length if necessary
    if len(introduction) > max_length:
        introduction = introduction[:max_length].strip() + "..."

    return introduction
