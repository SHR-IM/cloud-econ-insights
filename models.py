from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class User(db.Model):
    id            = db.Column(db.Integer, primary_key=True)
    email         = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    api_key_hash  = db.Column(db.String(255), nullable=True)
    created_at    = db.Column(db.DateTime, default=datetime.utcnow)

class Indicator(db.Model):
    id          = db.Column(db.Integer, primary_key=True)
    code        = db.Column(db.String(50), nullable=False)
    name        = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    created_at  = db.Column(db.DateTime, default=datetime.utcnow)

    user_id     = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    user        = db.relationship("User", backref="indicators")

class EconSnapshot(db.Model):
    id           = db.Column(db.Integer, primary_key=True)
    indicator_id = db.Column(db.Integer, db.ForeignKey("indicator.id"), nullable=False)
    indicator    = db.relationship("Indicator", backref="snapshots")

    user_id      = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    user         = db.relationship("User", backref="snapshots")

    country      = db.Column(db.String(3), nullable=False)
    year         = db.Column(db.Integer, nullable=False)
    value        = db.Column(db.Float, nullable=True)
    fetched_at   = db.Column(db.DateTime, default=datetime.utcnow)

