"""
Helper module for managing User model operations.

This module provides helper functions for performing operations related to the
User model, such as registering a new user with the given username.

Functions:
- register(username: str, db: SQLAlchemy = db) -> bool: Register a new user with
  the given username.

Classes:
- None

Exceptions:
- None
"""
from flask_sqlalchemy.extension import SQLAlchemy

from app import db, models


def register(
    username: str, email: str, password: str, session: SQLAlchemy = db.session
) -> bool:
    """
    Register a new user with the given username.

    Args:
        username (str): The username for the new user.
        email (str): The email for the new user.
        password (str): The password for the new user.
        db (SQLAlchemy, optional): The SQLAlchemy instance to use for database
        operations. Defaults to `db`.

    Returns:
        bool: True if the registration is successful, False otherwise.
    """
    try:
        user = models.User(
            username=username, email=email, username_lower=username.lower()
        )
        user.set_password(password)
        session.add(user)
        session.commit()
        return True
    except:
        session.rollback()
        return False
