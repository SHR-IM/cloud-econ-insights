from .auth_routes import auth_bp
from .indicators import indicators_bp
from .snapshots import snapshots_bp

def register_routes(app):
    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(indicators_bp, url_prefix="/indicators")
    app.register_blueprint(snapshots_bp, url_prefix="/snapshots")

