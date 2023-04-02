import datetime as dt


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
