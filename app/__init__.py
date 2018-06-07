from flask import Flask

from app.views import get_blueprints
from app.config import current_config


def init_server(env):
    server = Flask(__name__)

    # blueprintの設定
    blueprints = get_blueprints()
    for blueprint in blueprints:
        server.register_blueprint(blueprint)

    return server


def run(env):
    server = init_server(env=env)

    config = current_config('server')

    server.run(
        host=config.get('host'),
        port=config.get('port'),
        debug=config.get('debug')
    )
