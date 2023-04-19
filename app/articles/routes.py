from flask import flash, redirect, render_template, url_for
from flask_login import current_user

from app import db
from app.articles import bp
from app.models import Article


@bp.route("/")
def articles():
    if not current_user.is_authenticated:
        flash("You must be logged in to access that page.")
        return redirect(url_for("auth.login"))
