from flask_mdeditor import MDEditorField
from flask_wtf import FlaskForm
from wtforms.fields import BooleanField, StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired


class CreateArticleForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired()])
    summary = StringField("Summary", default="")
    # content = TextAreaField("Article Content", validators=[DataRequired()])
    content = MDEditorField("Article Content", validators=[DataRequired()])
    # image_url = StringField("Image")
    is_draft = BooleanField("Draft?", default=True)
    submit = SubmitField("Create article")


class EditArticleForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired()])
    summary = StringField("Summary", default="")
    # content = TextAreaField("Article Content", validators=[DataRequired()])
    content = MDEditorField("Article Content", validators=[DataRequired()])
    # image_url = StringField("Image")
    is_draft = BooleanField("Draft?")
    submit = SubmitField("Save")
