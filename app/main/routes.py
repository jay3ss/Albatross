from flask import flash, redirect, render_template, url_for
from flask_login import current_user, login_required

from app.main.albatross import compile_posts
from app import db, models
from app.decorators import own_resource_required
from app.main import bp, forms


@bp.route("/")
def index():
    if current_user.is_authenticated:
        return redirect(url_for("main.profile", username=current_user.username))
    return render_template("landing_page.html")


@bp.route("/u/<username>")
@login_required
@own_resource_required(redirect_route="main.index")
def profile(username):
    user = db.first_or_404(
        db.select(models.User).filter_by(username_lower=username.lower())
    )
    form = forms.CompileForm()
    return render_template("main/profile.html", user=user, form=form)


@bp.route("/u/<username>/update", methods=["get", "post"])
@login_required
@own_resource_required(redirect_route="main.index")
def update_profile(username):
    form = forms.EditUserForm()
    if form.validate_on_submit():
        form.populate_obj(current_user)
        if form.password.data:
            current_user.set_password(form.password.data)
        db.session.commit()
        flash("Your profile has been updated!", "success")
        return redirect(url_for("main.profile", username=current_user.username))

    user = db.first_or_404(
        db.select(models.User).filter_by(username_lower=username.lower())
    )
    form.username.data = user.username
    form.email.data = user.email
    form.about.data = user.about
    return render_template("main/update_profile.html", form=form, user=user)


@bp.route("/u/<username>/compile", methods=["get", "post"])
@login_required
@own_resource_required(redirect_route="main.index")
def compile_site(username):
    form = forms.CompileForm()
    if form.validate_on_submit():
        # What this should do:
        # 1. compile the user's articles (if any) to a static site into the "output"
        #    directory
        # 2. zip the "output" directory
        # 3. notify the user that the compilation (and zipping) is complete
        #   a. do it by email
        #   b. flash the user
        #   c. both? something else?
        user = models.User.query.filter_by(username_lower=username.lower()).first()
        output_path = compile_posts(articles=user.articles)
        return redirect(url_for("main.profile", username=username.lower()))
    return redirect(url_for("main.profile", username=username.lower()))
