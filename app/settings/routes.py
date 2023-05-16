from pathlib import Path

from flask import current_app, flash, json, render_template, send_file
from flask_login import current_user, login_required

from app.settings import bp, current_settings, forms


@bp.route("/settings")
@login_required
def settings():
    upload_form = forms.UserSettingsFileUploadForm()
    return render_template(
        "settings/settings.html",
        settings=str(current_settings),
        upload_form=upload_form
    )


@bp.route("/settings/upload", methods=["post"])
@login_required
def upload_settings():
    return ""


@bp.route("/settings/export", methods=["post"])
@login_required
def export():
    file_name = f"{current_user.username_lower}-settings.json"
    upload_path = Path(current_app.config["UPLOAD_FOLDER"]).resolve()
    settings_file_path = current_settings.write(upload_path/file_name)
    flash(f"Settings file successfully written to {file_name}.", "success")
    response = send_file(settings_file_path, as_attachment=True)
    return response
