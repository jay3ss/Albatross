import uuid

import mistune
from pygments import highlight
from pygments.formatters import html
from pygments.lexers import get_lexer_by_name
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



class HighlightRenderer(mistune.HTMLRenderer):
    """
    Custom renderer for syntax highlighting. Adapted from:
    https://mistune.lepture.com/en/v2.0.4/guide.html#customize-renderer
    """
    def block_code(self, code, lang=None):
        if lang:
            lexer = get_lexer_by_name(lang, stripall=True)
            formatter = html.HtmlFormatter()
            return highlight(code, lexer, formatter)
        return "<pre><code>" + mistune.escape(code) + "</code></pre>"
