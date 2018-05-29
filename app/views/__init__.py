from . import (
    user,
    thread,
    category,
)


blueprints = [
    user.app,
    thread.app,
    category.app,
]


def get_blueprints():
    return blueprints
