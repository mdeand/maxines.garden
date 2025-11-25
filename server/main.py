from dotenv import load_dotenv
from flask import Flask, send_from_directory
from shared.db import Db
from shared.env import Env
from . import e

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
            db = app.config["db"] = Db(Env().db_path)

    app.register_blueprint(e.blueprint)
    app.run()


if __name__ == "__main__":
    main()
