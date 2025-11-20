from flask import Flask, jsonify
from config import DevConfig
from models import db
from routes import register_routes

def create_app(config_class=DevConfig):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)

    @app.route("/")
    def home():
        return jsonify({"message": "Cloud Economics Insights API - it works!"})

    # Create DB tables (SQLite for now)
    with app.app_context():
        db.create_all()

    register_routes(app)
    return app

if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=5000, debug=True)

