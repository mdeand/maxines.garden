"""The formidable module e.py"""

from flask import Blueprint, current_app, render_template

blueprint = Blueprint("e", __name__, template_folder="../templates")


@blueprint.route("/everything")
def index():
    db = current_app.config["db"]
    entries = db.get_entries()

    return render_template("e-index.html", entries=entries)


@blueprint.route("/e/<slug>")
# NOTE(mdeand): Backward compatibility with old site.
@blueprint.route("/entries/<slug>")
def entry(slug: str):
    db = current_app.config["db"]
    entry = db.get_entry_by_slug(slug)

    if entry is None:
        return "<p>Entry not found.</p>", 404

    return entry[2]
