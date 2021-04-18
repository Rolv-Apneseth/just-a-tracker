from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func


USERNAME_MAX_LENGTH = 50

users_workspaces = db.Table(
    "users_wokspaces",
    db.Column("user_id", db.Integer, db.ForeignKey("user.user_id")),
    db.Column("workspace_id", db.Integer, db.ForeignKey("workspace.workspace_id")),
)


class Workspace(db.Model):
    workspace_id = db.Column(db.Integer, primary_key=True)
    project_name = db.Column(db.String(128))
    project_link = db.Column(db.String(320))

    author_id = db.Column(db.Integer, db.ForeignKey("user.user_id"))
    bugs = db.relationship("Bug", cascade="all, delete, delete-orphan")


class User(db.Model, UserMixin):
    user_id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(320), unique=True)
    password = db.Column(db.String(128))
    username = db.Column(db.String(USERNAME_MAX_LENGTH), unique=True)

    bugs = db.relationship("Bug")
    workspaces = db.relationship(
        "Workspace",
        secondary=users_workspaces,
        backref=db.backref("users", lazy="dynamic"),
    )

    # Override UserMixin method to return correct id value
    def get_id(self):
        return self.user_id


class Bug(db.Model):
    bug_id = db.Column(db.Integer, primary_key=True)
    bug_title = db.Column(db.String(64))
    bug_description = db.Column(db.String(1024))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    is_important = db.Column(db.Boolean, unique=False, default=False)
    is_open = db.Column(db.Boolean, unique=False, default=True)
    close_message = db.Column(db.String(248))

    author_id = db.Column(db.Integer, db.ForeignKey("user.user_id"))
    author_username = db.Column(db.String(USERNAME_MAX_LENGTH))
    workspace_id = db.Column(db.Integer, db.ForeignKey("workspace.workspace_id"))
