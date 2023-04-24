import pytest
from wtforms import ValidationError

from app.validators import UniqueEmail


def test_unique_email_validator_valid_data(session, dummy_form, dummy_field):
    email = "non-existent-email@example.com"
    dummy_field.data = email
    validator = UniqueEmail()


def test_unique_email_validator_invalid_data(session, dummy_form, dummy_field):
    email = "non-existent-email@example.com"
    dummy_field.data = email
    validator = UniqueEmail()

    with pytest.raises(ValidationError) as e:
        validator(dummy_form, dummy_field)

    message = "Email is already taken."
    assert str(e.value) == message

