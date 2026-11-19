"""Flask application factory for the academic economics API."""
import os

from flask import Flask, jsonify
from config import ProdConfig
from models import db
from routes import register_routes


def create_app(config_class=None):
    app = Flask(__name__)
    app.config.from_object(config_class or ProdConfig)

    db.init_app(app)
    app.url_map.strict_slashes = False

    @app.route("/")
    def home():
        return jsonify({"message": "Cloud Economics Insights API"})

    register_routes(app)
    with app.app_context():
        db.create_all()

    return app


if __name__ == "__main__":
    app = create_app()
    port = int(os.environ.get("PORT", "8080"))
    app.run(host="127.0.0.1", port=port, debug=False)
