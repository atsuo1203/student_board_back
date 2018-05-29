from . import (
    user,
    thread,
    category,
    university,
)


blueprints = [
    user.app,
    thread.app,
    category.app,
    university.app,
]


def get_blueprints():
    return blueprints
