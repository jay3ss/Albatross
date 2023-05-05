from flask_wtf import FlaskForm
from wtforms import BooleanField, PasswordField, StringField, SubmitField
from wtforms.validators import DataRequired, EqualTo, Email, Regexp, ValidationError

from app import models


class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    remember_me = BooleanField("Remember Me")
    submit = SubmitField("Sign in")


class RegistrationForm(FlaskForm):
    username = StringField(
        "Username",
        validators=[
            DataRequired(),
            Regexp(
                regex=r"^[\w-]+$",
                message=(
                    "Username must contain only alphanumeric "
                    "characters, underscores, or hyphens."
                ),
            ),
        ],
    )
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    password2 = PasswordField(
        "Confirm Password", validators=[DataRequired(), EqualTo("password")]
    )
    submit = SubmitField("Register")

    def validate_email(self, field):
        """
        Custom validator to check if the new email is already taken.
        """
        if models.User.is_email_taken(field.data.lower()):
            raise ValidationError("Email is already taken.")


class ResetPasswordRequestForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    submit = SubmitField("Submit")


class ResetPasswordForm(FlaskForm):
    password = PasswordField("Enter new password", validators=[DataRequired()])
    password2 = PasswordField(
        "Re-enter password", validators=[DataRequired(), EqualTo("password")]
    )
    submit = SubmitField("Submit")
