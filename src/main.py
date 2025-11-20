from dotenv import load_dotenv
from flask import Flask


app = Flask(__name__)


@app.route("/")
def hello_world():
    return "<p>Hello, Wfwordwdwdwdld!</p>"


def main():
    load_dotenv()
    app.run()


if __name__ == "__main__":
    main()
