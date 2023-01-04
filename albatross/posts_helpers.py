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


def generate_summary(post_contents: str, max_length: int = 300) -> str:
    """Generate a brief summary of a post based on its contents.

    Args:
        post_contents: The contents of the post.
        max_length: The maximum length of the summary.

    Returns:
        A brief summary of the post.
    """
    # Split the post contents into a list of sentences
    sentences = re.split(r"(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?)\s", post_contents)

    # Initialize the summary
    summary = ""

    # Add sentences to the summary until the summary is at least 90% of the maximum length
    for sentence in sentences:
        summary += sentence + " "
        if len(summary) >= max_length * 0.9:
            break

    # Trim the summary to the maximum length if necessary
    if len(summary) > max_length:
        summary = summary[:max_length] + "..."

    return summary
