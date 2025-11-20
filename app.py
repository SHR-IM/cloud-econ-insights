from flask import Flask, jsonify

def create_app():
    app = Flask(__name__)

    @app.route("/")
    def home():
        return jsonify({"message": "Cloud Economics Insights API - it works!"})

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=5000, debug=True)


