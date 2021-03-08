from flask import Blueprint, render_template
from flask_login import login_required, current_user

views = Blueprint("views", __name__)


@views.route("/")
def homepage():
    return render_template("home.html")


@views.route("/account")
@login_required
def account():
    return render_template("account.html")


@views.route("/create-workspace")
def create_workspace():
    return render_template("create_workspace.html")


@views.route("/workspace-hub")
def workspace_hub():
    return render_template("hub.html")


@views.route("/workspace")
def workspace():
    return render_template("workspace.html", project_id=1234563)
