import datetime as dt

from flask import Flask


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
    app.jinja_env.filters['datetime_format']: list = datetime_format

    return app
