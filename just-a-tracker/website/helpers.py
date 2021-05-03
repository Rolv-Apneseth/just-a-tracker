from flask import flash
from flask_login import current_user

from .models import Workspace, User, Bug, Comment, pretty_date


def add_bug_to_workspace(db, current_user, data, workspace_id):
    """Adds a bug object connected to the given workspace to the database."""

    workspace = Workspace.query.get(workspace_id)

    bug_info = {
        "bug_title": data.get("bug-title"),
        "bug_description": data.get("bug-description"),
        "author_id": current_user.user_id,
        "author_username": current_user.username,
        "workspace_id": workspace_id,
    }

    if bug_info["bug_title"] and bug_info["bug_description"]:
        if current_user in workspace.users:
            new_bug = Bug(**bug_info)
            db.session.add(new_bug)
            db.session.commit()

            # Add 'bug report opened' comment for the new bug report
            add_comment_to_bug(
                db,
                new_bug,
                workspace,
                f"Bug report opened by {current_user.username}",
                True,
            )

        else:
            flash("The current user does not have access to that workspace")


def add_user_to_workspace(db, data, workspace):
    """Adds given user to given workspace and commits the change."""

    user = User.query.filter_by(username=data.get("user-email")).first()
    if not user:
        user = User.query.filter_by(email=data.get("user-email")).first()

    if user:
        if user not in workspace.users:
            workspace.users.append(user)
            db.session.commit()

        else:
            flash("That user is already associated with this workspace.")
    else:
        flash("There is no user with that username or email address.")


def add_comment_to_bug(db, bug, workspace, text, is_action):
    """Adds a comment object to the given bug object and commits to the database."""

    if bug and text:
        if current_user in workspace.users:
            new_comment = Comment(
                content=text,
                is_action=is_action,
                bug_id=bug.bug_id,
                author_id=current_user.user_id,
                author_username=current_user.username,
            )

            db.session.add(new_comment)
            db.session.commit()

        else:
            flash("The current user does not have access to that workspace")


def add_action_comments(db, bug, workspace, make_open, make_important):
    """
    Adds an action comment to a given bug object if one or more
    of its attributes have been changed.
    """

    # List containing lists of conditions and their corresponding response to
    # give if true. Lists come in the format [condition, response if true]
    conditions_responses = [
        # Bug report closed
        [
            bug.is_open and not make_open,
            f"Closed by {current_user.username} on {pretty_date()}",
        ],
        # Bug report opened
        [
            not bug.is_open and make_open,
            f"Reopened by {current_user.username} on {pretty_date()}",
        ],
        # Bug report important mark removed
        [
            bug.is_important and not make_important,
            (
                f"Important mark removed by {current_user.username}"
                f" on {pretty_date()}"
            ),
        ],
        # Bug report marked as important
        [
            not bug.is_important and make_important,
            f"Marked important by {current_user.username} on {pretty_date()}",
        ],
    ]

    # Loop through conditions_responses and add an action comment with
    # the corresponding response if the condition is met
    for condition, response in conditions_responses:
        if condition:
            add_comment_to_bug(
                db,
                bug,
                workspace,
                response,
                True,
            )