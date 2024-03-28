from flask import Flask

from verse.routes import rag


def create_app(test_config=None):
    app = Flask(__name__)

    # configure application
    if not test_config:
        app.config.from_object("verse.config.Config")
    else:
        app.config.from_mapping(test_config)

    # register pulse route for heartbeats
    @app.route("/pulse")
    def pulse():
        return ""

    # register blueprints
    app.register_blueprint(rag.bp)

    return app