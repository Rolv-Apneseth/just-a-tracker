from flask import Blueprint


views = Blueprint("views", __name__)


@views.route("/")
def homepage():
    return "<h1>TEST</h1>"
