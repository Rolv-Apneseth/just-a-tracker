from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
import re

from . import db
from .models import User, Workspace, Bug


auth = Blueprint("auth", __name__)


# CONSTANTS
RE_USERNAME = r"^[\w-]{6,}$"
RE_PASSWORD = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[\w\W]{8,}$"

SIGN_UP_RESPONSES = {
    "pass_match": (
        "Your passwords did not match. Please make "
        "sure you type the same password in both fields."
    ),
    "pass_format": (
        "Your password must be at least 8 characters long and"
        " contain: 1 uppercase letter, 1 lowercase letter and"
        " 1 number"
    ),
    "user_format": (
        "Username must be 6 characters or longer, and can only "
        "include letters, numbers and the symbols '_' and '-'"
    ),
    "user_exists": "Sorry, an account with that username already exists.",
    "email_exists": "Sorry, an account with that email address already exists",
}


# HELPERS
def get_user_by_username(username):
    return User.query.filter_by(username=username).first()


def get_user_by_email(email):
    return User.query.filter_by(email=email).first()


def find_user(username):
    """Tries to get the user by username or email address and returns the result."""

    user = get_user_by_username(username)
    if not user:
        user = get_user_by_email(username)

    return user


def validate_sign_up_info(form):
    email = form.get("email")
    username = form.get("username")
    password = form.get("password")
    password_confirm = form.get("password-confirm")

    result = (
        True,
        {
            "email": email,
            "username": username,
            "password": generate_password_hash(password, method="sha256"),
        },
    )

    conditions = {
        "pass_match": password != password_confirm,
        "pass_format": not re.match(RE_PASSWORD, password),
        "user_format": not re.match(RE_USERNAME, username),
        "user_exists": get_user_by_username(username),
        "email_exists": get_user_by_email(email),
    }

    for key, condition in conditions.items():
        if condition:
            flash(SIGN_UP_RESPONSES[key])
            result = (False, {})

    return result


def validate_login_info(form):
    result = None

    username = form.get("username")
    password = form.get("password")

    user = find_user(username)

    if user:
        if check_password_hash(user.password, password):
            result = user

        else:
            flash("Password was incorrect. Please try again.")

    else:
        flash("No account matches that username or email.")

    return result


# ROUTES
@auth.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        validated_user = validate_login_info(request.form)

        if validated_user:
            # Login user
            login_user(validated_user, remember=True)
            return redirect(url_for("views.account"))

    return render_template("login.html", user=current_user)


@auth.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("auth.login"))


@auth.route("/sign-up", methods=["GET", "POST"])
def sign_up():
    if request.method == "POST":
        validated = validate_sign_up_info(request.form)

        if validated[0]:
            # Add user to database
            new_user = User(**validated[1])
            db.session.add(new_user)
            db.session.commit()

            # Login new user
            login_user(new_user, remember=True)

            return redirect(url_for("views.account"))

    return render_template("sign_up.html", user=current_user)


@auth.route("/workspace-hub", methods=["GET", "POST"])
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


@auth.route("/workspace/<workspace_id>", methods=["GET", "POST"])
@login_required
def workspace(workspace_id):
    workspace_object = Workspace.query.filter_by(workspace_id=workspace_id).first()

    if request.method == "POST":
        info = {
            "bug_title": request.form.get("bug-title"),
            "bug_description": request.form.get("bug-description"),
            "author_id": current_user.user_id,
            "author_username": current_user.username,
            "workspace_id": workspace_object.workspace_id,
        }

        if info["bug_title"] and info["bug_description"]:
            new_bug = Bug(**info)
            # new_bug.users.append(current_user)
            db.session.add(new_bug)
            db.session.commit()

    if workspace_object and current_user in workspace_object.users:
        return render_template(
            "workspace.html", workspace=workspace_object, user=current_user
        )

    flash("The requested workspace was not found, or you do not have access to it.")
    return redirect(url_for("auth.workspace-hub"))
