"""The formidable module e.py"""

from flask import Blueprint
from flask import current_app

blueprint = Blueprint("e", __name__, template_folder="templates")


@blueprint.route("/e")
@blueprint.route("/entries")
def index():
    return "<p>This is the e page.</p>"


@blueprint.route("/e/<slug>")
# NOTE(mdeand): Backward compatibility with old site.
@blueprint.route("/entries/<slug>")
def entry(slug: str):
    db = current_app.config["db"]
    entry = db.get_entry_by_slug(slug)

    if entry is None:
        return "<p>Entry not found.</p>", 404

    return entry[2]
