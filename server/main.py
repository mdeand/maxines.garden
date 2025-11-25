import os
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
    env = Env()

    with app.app_context():
        if app.config.get("db") is None:
            app.config["db"] = Db(env.db_path)

    app.register_blueprint(e.blueprint)
    
    match env.deployment_mode:
        case "Debug":
            app.run(port=5000, debug=True)
        case "Production":
            from waitress import serve
            serve(app, host="0.0.0.0", port=5000)

if __name__ == "__main__":
    main()
