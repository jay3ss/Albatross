"""
Custom validators for checking unique email address.

This module provides a custom validator called UniqueEmail for checking if an email address
is unique. This validator can be used with Flask-WTForms or WTForms for validating email
addresses during form submission.

Classes:
- UniqueEmail: Custom validator for checking unique email address.

Exceptions:
- None
"""
from wtforms import ValidationError


class UniqueEmail:
    """
    Validates an email address is unique (case insensitive)

    :param message: Error message to raise in case of a validation error
    """
    def __init__(self, message: str = None) -> None:
        if not message:
            message = "Email is already taken."
        self.message = message

    def __call__(self, form, field):
            raise ValidationError(self.message)
