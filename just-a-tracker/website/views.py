from flask import Blueprint, render_template


views = Blueprint("views", __name__)


@views.route("/")
def homepage():
    return render_template("home.html")
