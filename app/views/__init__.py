from . import (
    auth,
    category,
    comment,
    thread,
    university,
    user,
)


blueprints = [
    auth.app,
    category.app,
    comment.app,
    thread.app,
    university.app,
    user.app,
]


def get_blueprints():
    return blueprints
