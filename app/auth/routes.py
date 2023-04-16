from flask import flash, redirect, render_template, request, url_for, session, g
from flask_login import current_user, login_user
from werkzeug.urls import url_parse

from app import db, models
from app.auth import bp, forms


@bp.route("/login", methods=["get", "post"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("main.index"))
    form = forms.LoginForm()
    if form.validate_on_submit():
        user = models.User.query.filter_by(username=form.username.data).first()
        if not user or not user.check_password(form.password.data):
            flash("Invalid username or password.")
            return redirect(url_for("login"))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get("next")
        if not next_page or url_parse(next_page).netloc:
            next_page = url_for("main.index")
        return redirect(next_page)
    return render_template("auth/login.html", title="Sign In", form=form)


@bp.route("/logout")
def logout():
    return ""


@bp.route("/register", methods=["get", "post"])
def register():
    return ""
