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


# HELPERS
def validate_info(form):
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


# ROUTES
@auth.route("/login", methods=["GET", "POST"])
def login():
    return render_template("login.html")


@auth.route("/logout")
def logout():
    return "<p>Logout</p>"


@auth.route("/sign-up", methods=["GET", "POST"])
def sign_up():
    if request.method == "POST":
        validated = validate_info(request.form)

        if validated[0]:
            new_user = User(**validated[1])
            db.session.add(new_user)
            db.session.commit()

            return redirect(url_for("views.account"))

    return render_template("sign_up.html")
