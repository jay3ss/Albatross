from pathlib import Path

from flask import current_app, flash, json, redirect, render_template, send_file, url_for
from flask_login import current_user, login_required

from app import db
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
    upload_form = forms.UserSettingsFileUploadForm()
    if upload_form.validate_on_submit():
        filename = upload_form.file.data.filename
        with open(filename) as f:
            new_settings = json.load(f)

        current_settings.update(new_settings)
        db.session.commit()
        flash("File uploaded and applied successfully.", "success")
    return redirect(url_for("settings.settings"))


@bp.route("/settings/export", methods=["post"])
@login_required
def export():
    file_name = f"{current_user.username_lower}-settings.json"
    upload_path = Path(current_app.config["UPLOAD_FOLDER"]).resolve()
    settings_file_path = current_settings.write(upload_path/file_name)
    flash(f"Settings file successfully written to {file_name}.", "success")
    response = send_file(settings_file_path, as_attachment=True)
    return response
