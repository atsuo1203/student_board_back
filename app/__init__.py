from app.config import Config
from app.database import init_db
from flask import Flask
from .views import get_blueprints


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    init_db(app)

    blueprints = get_blueprints()
    for blueprint in blueprints:
        app.register_blueprint(blueprint)

    return app


app = create_app()
