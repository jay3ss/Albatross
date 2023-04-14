from flask import redirect, render_template
from flask_login import current_user

from app.auth import bp


@bp.route("/login", methods=["get", "post"])
def login():
    return "Login"


@bp.route("/logout")
def logout():
    return ""
