from flask import Blueprint, render_template
from flask_login import login_required, current_user

views = Blueprint("views", __name__)


@views.route("/")
def homepage():
    return render_template("home.html", user=current_user)


@views.route("/account")
@login_required
def account():
    return render_template("account.html", user=current_user)


@views.route("/create-workspace")
def create_workspace():
    return render_template("create_workspace.html", user=current_user)


@views.route("/workspace")
def workspace():
    return render_template("workspace.html", project_id=1234563, user=current_user)
