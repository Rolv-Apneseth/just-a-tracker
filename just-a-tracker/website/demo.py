from dataclasses import dataclass, field
from enum import Enum

from werkzeug.security import generate_password_hash

from .helpers import (add_action_comments, add_bug_to_workspace, add_user_to_workspace,
                      create_user, create_workspace, find_user)


@dataclass
class Comment:
    content: str
    by_collaborator: bool = False


@dataclass
class Bug:
    title: str
    description: str
    comments: list[Comment] = field(default_factory=list)
    open: bool = True
    important: str = False
    by_collaborator: bool = False


@dataclass
class Workspace:
    title: str
    bugs: list[Bug]
    by_collaborator: bool = False


def create_demo_user_data(db, demo_users):
    for workspace in DemoUserData.workspaces.value:
        author, collaborator = (
            demo_users[::-1] if workspace.by_collaborator else demo_users
        )

        new_workspace = create_workspace(
            db,
            author,
            {
                "project_name": workspace.title,
                "project_link": "",
            },
        )
        add_user_to_workspace(db, {"user-email": collaborator.email}, new_workspace)

        for bug in workspace.bugs:
            bug_author = demo_users[1] if bug.by_collaborator else demo_users[0]

            new_bug = add_bug_to_workspace(
                db,
                bug_author,
                {
                    "bug-title": bug.title,
                    "bug-description": bug.description,
                },
                new_workspace.workspace_id,
            )

            add_action_comments(
                db, bug_author, new_bug, new_workspace, bug.open, bug.important
            )


def get_demo_users(db):
    main = find_user(DemoUserData.email.value)
    if not main:
        main = create_user(
            db,
            {
                "email": DemoUserData.email.value,
                "username": DemoUserData.username.value,
                "password": generate_password_hash(
                    DemoUserData.password.value, method="sha256"
                ),
            },
        )

    collaborator = find_user(DemoUserData.collaborator.value)
    if not collaborator:
        collaborator = create_user(
            db,
            {
                "email": f"{DemoUserData.email.value[:-1]}.uk",
                "username": DemoUserData.collaborator.value,
                "password": generate_password_hash(
                    DemoUserData.password.value, method="sha256"
                ),
            },
        )

    return (main, collaborator)


def reset_demo_users(db):
    for user in get_demo_users(db):
        db.session.delete(user)

    db.session.commit()

    demo_users = get_demo_users(db)
    create_demo_user_data(db, demo_users)

    return demo_users


class DemoUserData(Enum):
    username = "John Smith"
    email = "realemail@iswear.com"
    password = "Password123"
    collaborator = "James Lee"
    workspaces = [
        Workspace(
            title="Main Project",
            bugs=[
                Bug(
                    title="Website loads too slowly",
                    description=(
                        "The website takes a full 1-2 minutes to load!"
                        "\n\nHow can we fix this?"
                    ),
                    comments=[
                        Comment(
                            content=(
                                "This is because this demo of the project is hosted"
                                "on Heroku, and if the site is not being used for a "
                                "while, the process is put to sleep and needs to be "
                                "restarted when the site is being accessed.\n"
                                "Nothing to be done about it unfortunately."
                            ),
                            by_collaborator=True,
                        )
                    ],
                    important=True,
                ),
                Bug(
                    title="Problem 2",
                    description="Lorem ipsum dolor sit amet consectetur, adipisicing "
                    "elit. Rem error sed, illum repudiandae accusamus quo similique "
                    "reprehenderit quasi et consequuntur.",
                    comments=[
                        Comment(
                            content="Lorem ipsum dolor sit amet consectetur, "
                            "adipisicing elit.",
                            by_collaborator=True,
                        ),
                        Comment(
                            content="Rem error sed, illum repudiandae accusamus quo "
                            "similique reprehenderit quasi et consequuntur.",
                        ),
                    ],
                    important=True,
                ),
                Bug(
                    title="Problem 3",
                    description="Lorem ipsum dolor sit amet consectetur, adipisicing "
                    "elit. Rem error sed, illum repudiandae accusamus quo similique "
                    "reprehenderit quasi et consequuntur.",
                    comments=[
                        Comment(
                            content="Lorem ipsum dolor sit amet consectetur, "
                            "adipisicing elit.",
                            by_collaborator=True,
                        ),
                        Comment(
                            content="Rem error sed, illum repudiandae accusamus quo "
                            "similique reprehenderit quasi et consequuntur.",
                        ),
                    ],
                ),
                Bug(
                    title="Problem 4",
                    description="Lorem ipsum dolor sit amet consectetur, adipisicing "
                    "elit. Rem error sed, illum repudiandae accusamus quo similique "
                    "reprehenderit quasi et consequuntur.",
                    comments=[
                        Comment(
                            content="Lorem ipsum dolor sit amet consectetur, "
                            "adipisicing elit.",
                            by_collaborator=True,
                        ),
                        Comment(
                            content="Rem error sed, illum repudiandae accusamus quo "
                            "similique reprehenderit quasi et consequuntur.",
                        ),
                    ],
                    by_collaborator=True,
                ),
                Bug(
                    title="Problem 5",
                    description="Lorem ipsum dolor sit amet consectetur, adipisicing "
                    "elit. Rem error sed, illum repudiandae accusamus quo similique "
                    "reprehenderit quasi et consequuntur.",
                    comments=[
                        Comment(
                            content="Lorem ipsum dolor sit amet consectetur, "
                            "adipisicing elit.",
                            by_collaborator=True,
                        ),
                    ],
                ),
                Bug(
                    title="Prolem 6",
                    description="Lorem ipsum dolor sit amet consectetur, adipisicing "
                    "elit. Rem error sed, illum repudiandae accusamus quo similique "
                    "reprehenderit quasi et consequuntur.",
                    comments=[
                        Comment(
                            content="Lorem ipsum dolor sit amet consectetur, "
                            "adipisicing elit.",
                            by_collaborator=True,
                        ),
                    ],
                    open=False,
                ),
                Bug(
                    title="Problem 7",
                    description="Lorem ipsum dolor sit amet consectetur, adipisicing "
                    "elit. Rem error sed, illum repudiandae accusamus quo similique "
                    "reprehenderit quasi et consequuntur.",
                    comments=[
                        Comment(
                            content="Lorem ipsum dolor sit amet consectetur, "
                            "adipisicing elit.",
                            by_collaborator=True,
                        ),
                        Comment(
                            content="Lorem ipsum dolor sit amet consectetur, "
                            "adipisicing elit.",
                        ),
                    ],
                    open=False,
                    by_collaborator=True,
                ),
                Bug(
                    title="Problem 8",
                    description="Lorem ipsum dolor sit amet consectetur, adipisicing "
                    "elit. Rem error sed, illum repudiandae accusamus quo similique "
                    "reprehenderit quasi et consequuntur.",
                    comments=[
                        Comment(
                            content="Lorem ipsum dolor sit amet consectetur, "
                            "adipisicing elit.",
                            by_collaborator=True,
                        ),
                    ],
                ),
                Bug(
                    title="Problem 9",
                    description="Lorem ipsum dolor sit amet consectetur, adipisicing "
                    "elit. Rem error sed, illum repudiandae accusamus quo similique "
                    "reprehenderit quasi et consequuntur.",
                    comments=[
                        Comment(
                            content="Lorem ipsum dolor sit amet consectetur, "
                            "adipisicing elit.",
                            by_collaborator=True,
                        ),
                        Comment(
                            content="Lorem ipsum dolor sit amet consectetur, "
                            "adipisicing elit.",
                        ),
                    ],
                    important=True,
                ),
                Bug(
                    title="Problem 10",
                    description="Lorem ipsum dolor sit amet consectetur, adipisicing "
                    "elit. Rem error sed, illum repudiandae accusamus quo similique "
                    "reprehenderit quasi et consequuntur.",
                    comments=[
                        Comment(
                            content="Lorem ipsum dolor sit amet consectetur, "
                            "adipisicing elit.",
                            by_collaborator=True,
                        ),
                    ],
                    open=False,
                    by_collaborator=True,
                ),
            ],
        ),
        Workspace(
            title="Side Project 1",
            by_collaborator=True,
            bugs=[
                Bug(
                    title="Problem 1",
                    description="Lorem ipsum dolor sit amet consectetur, adipisicing "
                    "elit. Rem error sed, illum repudiandae accusamus quo similique "
                    "reprehenderit quasi et consequuntur.",
                    important=True,
                    by_collaborator=True,
                ),
                Bug(
                    title="Problem 2",
                    description="Lorem ipsum dolor sit amet consectetur, adipisicing "
                    "elit. Rem error sed, illum repudiandae accusamus quo similique "
                    "reprehenderit quasi et consequuntur.",
                ),
                Bug(
                    title="Problem 3",
                    description="Lorem ipsum dolor sit amet consectetur, adipisicing "
                    "elit. Rem error sed, illum repudiandae accusamus quo similique "
                    "reprehenderit quasi et consequuntur.",
                    by_collaborator=True,
                ),
                Bug(
                    title="Problem 4",
                    description="Lorem ipsum dolor sit amet consectetur, adipisicing "
                    "elit. Rem error sed, illum repudiandae accusamus quo similique "
                    "reprehenderit quasi et consequuntur.",
                    important=True,
                    by_collaborator=True,
                ),
                Bug(
                    title="Problem 5",
                    description="Lorem ipsum dolor sit amet consectetur, adipisicing "
                    "elit. Rem error sed, illum repudiandae accusamus quo similique "
                    "reprehenderit quasi et consequuntur.",
                    open=False,
                ),
            ],
        ),
    ]
