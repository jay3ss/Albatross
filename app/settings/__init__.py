from flask import Blueprint, g, has_request_context
from flask_login import current_user
from werkzeug.local import LocalProxy

from app import models


current_settings = LocalProxy(lambda: _get_settings())


def _get_settings() -> models.UserSettings:
    if has_request_context():
        if "_login_user" in g:
            settings = models.UserSettings.query.filter_by(user=current_user).first()
            return settings

    return None


bp = Blueprint("settings", __name__)


from app.settings import routes
