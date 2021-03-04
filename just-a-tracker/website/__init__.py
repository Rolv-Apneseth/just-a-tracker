import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
DB_NAME = "database.db"


def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = os.environ["JUST_A_TRACKER_KEY"]
    app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{DB_NAME}"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.init_app(app)

    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix="/")
    app.register_blueprint(auth, url_prefix="/")

    from .models import (
        users_workspaces,
        Workspace,
        User,
        Bug,
    )

    create_database(app)

    return app


def create_database(app):
    if not os.path.exists(os.path.join("website", DB_NAME)):
        db.create_all(app=app)
        print("Database created")
