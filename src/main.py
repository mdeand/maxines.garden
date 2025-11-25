import os
from dotenv import load_dotenv
from flask import Flask
from flask import send_from_directory

from db import Db
import content
import e

app = Flask(__name__)

@app.route("/dist/<path:path>")
def send_dist(path):
    # TODO: have a dist directory config? 
    return send_from_directory("../dist", path)

@app.route("/")
def index():
    return "<p>Hello, Wfwordwdwdwdld!</p>"


def main():
    load_dotenv()

    with app.app_context():
        if app.config.get("db") is None:
            db = app.config["db"] = Db(os.getenv("DATABASE_URL") or ".db.sqlite3")

        content.register(db)

    app.register_blueprint(
        e.blueprint,
    )
    app.run()


if __name__ == "__main__":
    main()
