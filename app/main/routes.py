from flask import flash, redirect, render_template, url_for
from flask_login import current_user, login_required

from app import db, models
from app.main import bp, forms


@bp.route("/")
def index():
    if current_user.is_authenticated:
        return redirect(url_for("main.profile", username=current_user.username))
    return render_template("landing_page.html")


@bp.route("/u/<username>")
@login_required
def profile(username):
    user = db.first_or_404(db.select(models.User).filter_by(
        username_lower=username.lower())
    )
    return render_template("main/profile.html", user=user)


@bp.route("/u/<username>/update", methods=["get", "post"])
@login_required
def update_profile(username):
    form = forms.EditUserForm()
    if form.validate_on_submit():
        form.populate_obj(current_user)
        if form.password.data:
            current_user.set_password(form.password.data)
        db.session.commit()
        flash("Your profile has been updated!", "success")
        return redirect(url_for("main.profile", username=current_user.username))

    user: models.User = db.first_or_404(
        db.select(models.User).filter_by(username_lower=username.lower())
    )
    form.username.data = user.username
    form.email.data = user.email
    form.about.data = user.about
    return render_template("main/update_profile.html", form=form, user=user)
