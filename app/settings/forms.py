from flask_wtf import FlaskForm
from wtforms import FileField, SubmitField

from wtforms.validators import DataRequired


class UserSettingsFileForm(FlaskForm):
    file_name = FileField("Choose a file", validators=[DataRequired()])
    submit = SubmitField("Submit")
