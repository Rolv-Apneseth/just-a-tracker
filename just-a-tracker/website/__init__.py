import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

db = SQLAlchemy()
DB_NAME = "database.db"


def create_app():
    # Set up app
    app = Flask(__name__)
    app.config["SECRET_KEY"] = os.environ["JUST_A_TRACKER_KEY"]
    app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{DB_NAME}"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    # app.config["SEND_FILE_MAX_AGE_DEFAULT"] = -1
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

    # Create database
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
