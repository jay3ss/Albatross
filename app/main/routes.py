from flask import render_template, redirect, url_for
from flask_login import current_user

from app.main import bp


@bp.route("/")
def index():
    if current_user.is_authenticated:
        return redirect(url_for("articles.articles"))
    return render_template("landing_page.html")
