from flask import Blueprint, render_template, request, flash
import re


auth = Blueprint("auth", __name__)


# CONSTANTS
RE_USERNAME = r"^[\w-]{6,}$"
RE_PASSWORD = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[\w\W]{8,}$"


@auth.route("/login", methods=["GET", "POST"])
def login():
    return render_template("login.html")


@auth.route("/logout")
def logout():
    return "<p>Logout</p>"


@auth.route("/sign-up", methods=["GET", "POST"])
def sign_up():
    if request.method == "POST":
        form = request.form
        email = form.get("email")
        username = form.get("username")
        password = form.get("password")
        password_confirm = form.get("password-confirm")

        if password != password_confirm:
            flash(
                "Your passwords did not match. Please make "
                "sure you type the same password in both fields.",
            )

        if not re.match(RE_PASSWORD, password):
            flash(
                "Your password must be at least 8 characters long and"
                " contain: 1 uppercase letter, 1 lowercase letter and"
                " 1 number"
            )

        if not re.match(RE_USERNAME, username):
            flash(
                "Username must be 6 characters or longer, and can only "
                "include letters, numbers and the symbols '_' and '-'"
            )

    return render_template("sign_up.html")
