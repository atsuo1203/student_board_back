from . import (
    user,
    thread,
    category,
    university,
    auth,
)


blueprints = [
    user.app,
    thread.app,
    category.app,
    university.app,
    auth.app,
]


def get_blueprints():
    return blueprints
