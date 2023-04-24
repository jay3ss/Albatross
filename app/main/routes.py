from flask import render_template, redirect, url_for
from flask_login import current_user, login_required

from app import db, models
from app.main import bp


@bp.route("/")
def index():
    if current_user.is_authenticated:
        return redirect(url_for("main.profile", username=current_user.username))
    return render_template("landing_page.html")


@bp.route("/u/<username>")
@login_required
def profile(username):
    user = db.first_or_404(db.select(models.User).filter_by(username=username))
    return render_template("main/profile.html", user=user)
