from . import (
    user
)


blueprints = [
    user.app,
]


def get_blueprints():
    return blueprints
