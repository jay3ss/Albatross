from unittest.mock import patch

import pytest
from wtforms import ValidationError

from app import models
from app.validators import UniqueEmail


def test_unique_email_validator_valid_data(dummy_form, dummy_field):
    email = "non-existent-email@example.com"
    dummy_field.data = email
    validator = UniqueEmail()

    with patch.object(models.User, 'is_email_taken', return_value=False):
        validator(dummy_form, dummy_field)


def test_unique_email_validator_invalid_data(dummy_form, dummy_field):
    email = "non-existent-email@example.com"
    dummy_field.data = email
    validator = UniqueEmail()

    with patch.object(models.User, 'is_email_taken', return_value=True):
        with pytest.raises(ValidationError) as e:
            validator(dummy_form, dummy_field)

    message = "Email is already taken."
    assert str(e.value) == message

