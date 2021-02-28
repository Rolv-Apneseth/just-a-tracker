import os
from flask import Flask


def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = os.environ["JUST_A_TRACKER_KEY"]

    return app
