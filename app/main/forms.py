from flask_login import current_user
from flask_wtf import FlaskForm
from wtforms import (EmailField, PasswordField, StringField, SubmitField,
                     TextAreaField, ValidationError)
from wtforms.validators import Length, Email, EqualTo

from app import models


class EditUserForm(FlaskForm):
    username = StringField("Username")
    about = TextAreaField("About me", validators=[Length(max=280)])
    email = EmailField("Email", validators=[Email()])
    password = PasswordField("Password")
    password2 = PasswordField("Retype Password", validators=[EqualTo("password")])
    submit = SubmitField("Update")

    def validate_username(self, field):
        """
        Custom validator to check if the new username is already taken.
        """
        user = models.User.query.filter_by(username=field.data).first()
        if user is not None and user.id != current_user.id:
            raise ValidationError('Username is already taken.')

    def validate_email(self, field):
        """
        Custom validator to check if the new email is already taken.
        """
        user = models.User.query.filter_by(email=field.data).first()
        if user is not None and user.id != current_user.id:
            raise ValidationError('Email is already taken.')
