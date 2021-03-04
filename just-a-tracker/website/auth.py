from flask import Blueprint, render_template, request, flash, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
import re

from . import db
from .models import User


auth = Blueprint("auth", __name__)


# CONSTANTS
RE_USERNAME = r"^[\w-]{6,}$"
RE_PASSWORD = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[\w\W]{8,}$"

PASS_MATCH = (
    "Your passwords did not match. Please make "
    "sure you type the same password in both fields."
)
PASS_FORMAT = (
    "Your password must be at least 8 characters long and"
    " contain: 1 uppercase letter, 1 lowercase letter and"
    " 1 number"
)
USER_FORMAT = (
    "Username must be 6 characters or longer, and can only "
    "include letters, numbers and the symbols '_' and '-'"
)
USER_EXISTS = "Sorry, an account with that username already exists."
EMAIL_EXISTS = "Sorry, an account with that email address already exists"


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

    if get_user_by_username(username):
        flash(USER_EXISTS)
        result = (False, {})

    if get_user_by_email(email):
        flash(EMAIL_EXISTS)
        result = (False, {})

    if password != password_confirm:
        flash(PASS_MATCH)
        result = (False, {})

    if not re.match(RE_PASSWORD, password):
        flash(PASS_FORMAT)
        result = (False, {})

    if not re.match(RE_USERNAME, username):
        flash(USER_FORMAT)
        result = (False, {})

    return result


def validate_login_info(form):
    username = form.get("username")
    password = form.get("password")

    result = (True, username)

    user = find_user(username)

    # Check password
    if user:
        if check_password_hash(user.password, password):
            pass  # login
        else:
            flash("Password was incorrect. Please try again.")
            result = (False, None)
    else:
        flash("No account matches that username or email")
        result = (False, None)

    return result


# ROUTES
@auth.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        validated = validate_login_info(request.form)

    return render_template("login.html")


@auth.route("/logout")
def logout():
    return "<p>Logout</p>"


@auth.route("/sign-up", methods=["GET", "POST"])
def sign_up():
    if request.method == "POST":
        validated = validate_sign_up_info(request.form)

        if validated[0]:
            new_user = User(**validated[1])
            db.session.add(new_user)
            db.session.commit()

            return redirect(url_for("views.account"))

    return render_template("sign_up.html")
