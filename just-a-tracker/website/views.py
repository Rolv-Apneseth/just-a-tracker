from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify
from flask_login import login_required, current_user
import json

from . import db
from .models import Workspace, Bug, User

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


def add_user_to_workspace(db, data, workspace):
    """Adds given user to given workspace and commits the change."""

    user = User.query.filter_by(username=data.get("user-email")).first()
    if not user:
        user = User.query.filter_by(email=data.get("user-email")).first()

    if user:
        if user not in workspace.users:
            workspace.users.append(user)
            db.session.commit()

        else:
            flash("That user is already associated with this workspace.")
    else:
        flash("There is no user with that username or email address.")


# ROUTES
@views.route("/")
def homepage():
    return render_template("home.html", user=current_user)


@views.route("/account")
@login_required
def account():
    return render_template("account.html", user=current_user)


@views.route("/create-workspace")
@login_required
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

        if data.get("user-email"):
            add_user_to_workspace(db, data, workspace_object)
        else:
            add_bug_to_workspace(db, current_user, data, workspace_id)

    if workspace_object and current_user in workspace_object.users:
        return render_template(
            "workspace.html",
            workspace=workspace_object,
            workspace_bugs_reversed=reversed(workspace_object.bugs),
            user=current_user,
            url=url_for("views.workspace", workspace_id=workspace_id),
        )

    flash("The requested workspace was not found, or you do not have access to it.")
    return redirect(url_for("views.workspace_hub"))


@views.route("/remove-user", methods=["POST"])
@login_required
def remove_user():
    data = json.loads(request.data)
    workspace_id = int(data["workspaceID"])
    user_id = int(data["userID"])

    workspace = Workspace.query.get(workspace_id)
    user = User.query.get(user_id)

    if user and workspace:
        has_permission = (
            workspace.author_id == current_user.user_id
            or user_id == current_user.user_id
        )

        if has_permission:
            if user_id != workspace.author_id:
                workspace.users.remove(user)
                db.session.commit()
            else:
                flash("Owner cannot be removed from the workspace.")
        else:
            flash(
                f"You do not have permission to remove {user.username}"
                f" from {workspace.project_name}!"
            )

    return jsonify({})


@views.route("/mark-bug", methods=["POST"])
@login_required
def mark_bug():
    data = json.loads(request.data)

    bug_id = data.get("bugID")
    bug = Bug.query.get(bug_id)
    workspace = Workspace.query.get(bug.workspace_id)

    make_open = False if data.get("makeOpen") == "false" else True
    make_important = False if data.get("makeImportant") == "false" else True

    if workspace and current_user in workspace.users:
        bug.is_open = make_open
        bug.is_important = make_important
        db.session.commit()

    return jsonify({})


@views.route("/delete-bug", methods=["POST"])
@login_required
def delete_bug():
    data = json.loads(request.data)
    bug_id = int(data.get("bugID"))

    bug = Bug.query.get(bug_id)
    if bug:
        workspace = Workspace.query.get(bug.workspace_id)

        has_permission = (
            current_user.user_id == workspace.author_id
            or current_user.user_id == bug.author_id
        )

        if has_permission:
            db.session.delete(bug)
            db.session.commit()
        else:
            flash(
                "You do not have permission to remove this bug report from "
                f"the workspace for {workspace.project_name}."
            )
    else:
        flash(f"Bug with id {bug.bug_id} not found.")

    return jsonify({})
