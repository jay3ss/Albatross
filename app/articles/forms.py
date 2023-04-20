from flask_wtf import FlaskForm
from wtforms.fields import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired


class CreateArticleForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired()])
    summary = StringField("Summary", default="")
    content = TextAreaField("Article Content", validators=[DataRequired()])
    # image_url = StringField("Image")
    submit = SubmitField("Create article")
