from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func


users_workspaces = db.Table(
    "users_wokspaces",
    db.Column("user_id", db.Integer, db.ForeignKey("user.user_id")),
    db.Column("workspace_id", db.Integer, db.ForeignKey("workspace.workspace_id")),
)


class Workspace(db.Model):
    workspace_id = db.Column(db.Integer, primary_key=True)
    project_name = db.Column(db.String(128))
    project_link = db.Column(db.String(320))

    bugs = db.relationship("Bug")


class User(db.Model, UserMixin):
    user_id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(320), unique=True)
    password = db.Column(db.String(128))
    username = db.Column(db.String(50), unique=True)

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

    author_id = db.Column(db.Integer, db.ForeignKey("user.user_id"))
    author_username = db.Column(db.String(50))
    workspace_id = db.Column(db.Integer, db.ForeignKey("workspace.workspace_id"))
