from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func


users_workspaces = db.Table(
    "users_wokspaces",
    db.Column("user_id", db.Integer, db.ForeignKey("user.id")),
    db.Column("workspace_id", db.Integer, db.ForeignKey("workspace.id")),
)

bugs_workspaces = db.Table(
    "bugs_workspaces",
    db.Column("bug_id", db.Integer, db.ForeignKey("bug.id")),
    db.Column("workspace_id", db.Integer, db.ForeignKey("workspace.id")),
)


class Workspace(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    project_name = db.Column(db.String(128), unique=True)


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(320), unique=True)
    password = db.Column(db.String(128))
    username = db.Column(db.String(50))
    bugs = db.relationship("Bug")
    workspaces = db.relationship(
        "Workspace",
        secondary=users_workspaces,
        backref=db.backref("users", lazy="dynamic"),
    )


class Bug(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    bug_title = db.Column(db.String(128))
    bug_description = db.Column(db.String(512))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    author_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    workspaces = db.relationship(
        "Workspace",
        secondary=users_workspaces,
        backref=db.backref("users", lazy="dynamic"),
    )
