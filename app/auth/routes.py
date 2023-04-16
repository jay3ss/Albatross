from flask import redirect, render_template, request, url_for
from flask_login import current_user, login_user

from app import db, models
from app.auth import bp, forms


@bp.route("/login", methods=["get", "post"])
def login():
    form = forms.LoginForm()
    if form.validate_on_submit():
        user = models.User.query.filter_by(username=form.username.data).first()
        if not user or not user.check_password(form.password.data):
            pass
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get("next")
        return redirect(url_for("main.index"))
    return render_template("auth/login.html", form=form)


@bp.route("/logout")
def logout():
    return ""


@bp.route("/register", methods=["get", "post"])
def register():
    return ""
