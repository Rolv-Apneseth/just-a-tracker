from flask import Blueprint, render_template, request, flash


auth = Blueprint("auth", __name__)


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
        else:
            pass

    return render_template("sign_up.html")
