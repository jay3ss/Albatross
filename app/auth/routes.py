from flask import flash, redirect, render_template, request, url_for
from flask_login import current_user, login_user, logout_user
from werkzeug.urls import url_parse

from app import db, models
from app.auth import bp, email, forms
from app.helpers import users as uh


@bp.route("/login", methods=["get", "post"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("main.index"))  # pragma: no cover

    form = forms.LoginForm()
    if form.validate_on_submit():
        user = models.User.query.filter_by(
            username_lower=form.username.data.lower()
        ).first()
        if not user or not user.check_password(form.password.data):
            flash("Incorrect username or password.", "danger")
            return redirect(url_for("auth.login"))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get("next")

        if not next_page or url_parse(next_page).netloc:
            next_page = url_for("main.index")
        return redirect(next_page)
    return render_template("auth/login.html", title="Sign In", form=form)


@bp.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("main.index"))


@bp.route("/register", methods=["get", "post"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("main.index"))

    form = forms.RegistrationForm()
    if form.validate_on_submit():
        successful_registration = uh.register(
            username=form.username.data,
            email=form.email.data,
            password=form.password.data,
            session=db.session,
        )
        if not successful_registration:
            flash("A user with that name or email already exists.", "danger")
        else:
            flash("Congratulations, you are now a registered user!", "success")
            return redirect(url_for("auth.login"))
    return render_template("auth/register.html", form=form, title="Register")


@bp.route("/reset_password", methods=["get", "post"])
def reset_password_request():
    if current_user.is_authenticated:
        return redirect("main.index")

    form = forms.ResetPasswordRequestForm()
    if form.validate_on_submit():
        user = models.User.query.filter_by(email=form.email.data.lower()).first()
        if user:
            email.send_password_reset_email(user)
        flash("Check your email for the instructions to reset your password")
        return redirect(url_for("auth.login"))

    return render_template(
        "auth/reset_password_request.html", title="Reset Password", form=form
    )


@bp.route("/reset_password/<token>", methods=["get", "post"])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for("main.index"))
    user: models.User = models.User.verify_reset_password_token(token)
    if not user:
        return redirect(url_for("main.index"))
    form = forms.ResetPasswordForm()
    if form.validate_on_submit():
        user.set_password(form.password.data)
        db.session.commit()
        flash("Your password has been reset.")
        return redirect(url_for("auth.login"))
    return render_template(
        "auth/reset_password.html", title="Reset Password", form=form
    )
