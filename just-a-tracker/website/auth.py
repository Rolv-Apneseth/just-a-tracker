from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
import re
import json

from . import db
from .models import User


auth = Blueprint("auth", __name__)


# CONSTANTS
RE_USERNAME = r"^[\w-]{6,}$"
RE_PASSWORD = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[\w\W]{8,}$"

WRONG_PASS_RESPONSE = "Password was incorrect. Please try again."
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
            flash(WRONG_PASS_RESPONSE)

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


@auth.route("/change-password", methods=["POST"])
@login_required
def change_password():
    # Assign data from form
    form = request.form
    current_password = form.get("current-password")
    new_password = form.get("new-password")
    confirm_new_password = form.get("confirm-new-password")

    # Password checks
    if not check_password_hash(current_user.password, current_password):
        flash(WRONG_PASS_RESPONSE)
    elif not re.match(RE_PASSWORD, new_password):
        flash(SIGN_UP_RESPONSES["pass_format"])
    elif new_password != confirm_new_password:
        flash(SIGN_UP_RESPONSES["pass_match"])
    elif new_password == current_password:
        flash("Your new password cannot be the same as your old password.")

    # Change user password if all checks passed
    else:
        current_user.password = generate_password_hash(new_password, method="sha256")
        db.session.commit()
        flash("Your password has been changed.")

    return redirect(url_for("views.account"))


@auth.route("/change-email", methods=["POST"])
@login_required
def change_email():
    # Assign data from form
    form = request.form
    password = form.get("change-email-password")
    new_email = form.get("new-email")
    confirm_new_email = form.get("confirm-new-email")

    # Perform checks
    if not check_password_hash(current_user.password, password):
        flash(WRONG_PASS_RESPONSE)
    elif not new_email == confirm_new_email:
        flash("Your emails did not match. Make sure you enter the same in both fields.")
    elif new_email == current_user.email:
        flash(f"Your email is already set to {new_email}")

    # If all checks passed, change users email address
    else:
        current_user.email = new_email
        db.session.commit()
        flash(f"The email address for your account has been changed to {new_email}.")

    return redirect(url_for("views.account"))
