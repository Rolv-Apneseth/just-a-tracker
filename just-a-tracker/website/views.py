from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify
from flask_login import login_required, current_user
import json

from . import db
from .models import Workspace, Bug


views = Blueprint("views", __name__)


# HELPER FUNCTIONS
def add_bug_to_workspace(db, current_user, data, workspace_id):
    """Adds a bug object connected to the given workspace to the database."""

    info = {
        "bug_title": data.get("bug-title"),
        "bug_description": data.get("bug-description"),
        "author_id": current_user.user_id,
        "author_username": current_user.username,
        "workspace_id": workspace_id,
    }

    if info["bug_title"] and info["bug_description"]:
        new_bug = Bug(**info)
        db.session.add(new_bug)
        db.session.commit()


# ROUTES
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


@views.route("/workspace-hub", methods=["GET", "POST"])
@login_required
def workspace_hub():
    if request.method == "POST":

        info = {
            "project_name": request.form.get("project-name"),
            "project_link": request.form.get("project-link"),
        }

        if info["project_name"]:
            new_workspace = Workspace(**info)
            new_workspace.users.append(current_user)
            new_workspace.author_id = current_user.user_id
            db.session.add(new_workspace)
            db.session.commit()

    return render_template("hub.html", user=current_user)


@views.route("/delete-workspace", methods=["POST"])
@login_required
def delete_workspace():
    workspace_id = json.loads(request.data)["workspaceID"]
    workspace = Workspace.query.get(workspace_id)

    if workspace:
        if workspace.author_id == current_user.user_id:
            db.session.delete(workspace)
            db.session.commit()
            return jsonify({})


@views.route("/workspace/<workspace_id>", methods=["GET", "POST"])
@login_required
def workspace(workspace_id):
    workspace_object = Workspace.query.filter_by(workspace_id=workspace_id).first()

    if request.method == "POST":
        data = request.form

        if data.get("collaborator"):
            pass
        else:
            add_bug_to_workspace(db, current_user, data, workspace_id)

    if workspace_object and current_user in workspace_object.users:
        return render_template(
            "workspace.html", workspace=workspace_object, user=current_user
        )

    flash("The requested workspace was not found, or you do not have access to it.")
    return redirect(url_for("auth.workspace-hub"))
