import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager


# CONSTANTS
DB_NAME = "database.db"
LOCAL_DATABASE_PATH = os.path.join("website", DB_NAME)


db = SQLAlchemy()


def create_app():
    # Set up app
    app = Flask(__name__)
    app.config["SECRET_KEY"] = os.environ["JUST_A_TRACKER_KEY"]
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    ENV = os.environ["JUST_A_TRACKER_ENV"]
    if ENV == "dev":
        app.debug = True
        app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{DB_NAME}"
    elif ENV == "prod":
        app.config["SQLALCHEMY_DATABASE_URI"] = os.environ["DATABASE_URL"]

    db.init_app(app)

    # Login Manager
    login_manager = LoginManager()
    login_manager.login_view = "auth.login"
    login_manager.init_app(app)

    # user_loader callback for login manager
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # Load blueprints
    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix="/")
    app.register_blueprint(auth, url_prefix="/")

    # Import database models
    from .models import (
        users_workspaces,
        Workspace,
        User,
        Bug,
    )

    # Create local database if it does not yet exist
    if ENV == "dev":
        create_database(app)

    return app


def create_database(app):
    if not os.path.exists(LOCAL_DATABASE_PATH):
        db.create_all(app=app)
        print("Local database created")
