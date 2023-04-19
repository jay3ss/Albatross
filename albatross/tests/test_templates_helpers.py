import datetime as dt
from albatross.helpers.templates import datetime_format


def test_datetime_format_default_format():
    dt_obj = dt.datetime(2023, 4, 1, 12, 30)
    formatted = datetime_format(dt_obj)
    assert formatted == "April 1, 2023"


def test_datetime_format_custom_format():
    dt_obj = dt.datetime(2023, 4, 1, 12, 30)
    formatted = datetime_format(dt_obj, "%B %d, %Y")
    assert formatted == "April 01, 2023"
