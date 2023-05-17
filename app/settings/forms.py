import json
import os
import sys
import traceback as tb

from flask import current_app
from flask_wtf import FlaskForm
from werkzeug.utils import secure_filename
from wtforms import FileField, SubmitField
from wtforms.validators import DataRequired, ValidationError


class UserSettingsFileUploadForm(FlaskForm):
    file = FileField("Choose a file", validators=[DataRequired()])
    submit = SubmitField("Submit")

    def validate_file(self, field):
        file = field.data
        file_extension = os.path.splitext(secure_filename(file.filename))[-1]
        file_extensions = current_app.config["UPLOAD_EXTENSIONS"]
        if file_extension not in file_extensions:
            raise ValidationError("Incorrect file type.")

        try:
            file.stream.seek(0)
            json.loads(file.stream.read().decode("utf-8"))
        except (json.JSONDecodeError, TypeError) as e:
            exc_type, exc_value, exc_tb = sys.exc_info()
            tbe = tb.TracebackException(
                exc_type,
                exc_value,
                exc_tb,
            )
            print("".join(tbe.format()), flush=True)
            raise ValidationError("Not a proper JSON file.")
