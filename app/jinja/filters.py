import datetime as dt

from flask import Flask
from pygments import highlight
from pygments.formatters import html
from pygments.lexers import get_lexer_by_name


def datetime_format(value: dt.datetime, format: str = "%B %-d, %Y") -> str:
    """
    Formats a datetime object as a string using the specified format.

    Args:
        value (dt.datetime): The datetime object to format.
        format (str, optional): A string specifying the format to use.
            This should be a valid strftime format string. Defaults to
            "%B %-d, %Y".

    Returns:
        str: A string representing the formatted datetime object.

    Adapted from:
    https://jinja.palletsprojects.com/en/3.1.x/api/#custom-filters
    """
    return value.strftime(format)


def highlight_syntax(code: str, lang: str = "python", style: str = "monokai") -> str:
    """
    Highlights the code block with the given style

    Args:
        code (str): The code to highlight.
        lang (str, optional): The language. Defaults to "python."
        style (str, optional): The style to use. Defaults to "monokai."

    Returns:
        str: The code with the syntax highlighted.

    Adapted from:
    https://gist.github.com/deepns/22d366709a96f9e6fceba8abc8bdb156
    """
    return highlight(
        code=code,
        lexer=get_lexer_by_name(lang),
        formatter=html.HtmlFormatter()
    )


def register_filters(app: Flask) -> Flask:
    """
    Register the custom filters

    Args:
        app (Flask): the app

    Returns:
        Flask: the app with the custom filters registered

    Adapted from:
    https://abstractkitchen.com/blog/how-to-create-custom-jinja-filters-in-flask/
    """
    app.jinja_env.filters["datetime_format"]: list = datetime_format
    app.jinja_env.filters["highlight_syntax"] = highlight_syntax

    return app
