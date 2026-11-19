"""Regression tests for authentication and tenant isolation.

Run: python -m unittest discover -s tests -v
"""
import hashlib
import unittest

from app import create_app
from models import User, db


class TestConfig:
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite://"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = "testing-only"


class APISecurityTests(unittest.TestCase):
    def setUp(self):
        self.app = create_app(TestConfig)
        self.client = self.app.test_client()
        self.context = self.app.app_context()
        self.context.push()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.context.pop()

    def register(self, name):
        response = self.client.post(
            "/auth/register",
            json={"email": f"{name}@example.com", "password": "test-pass-123"},
        )
        self.assertEqual(response.status_code, 201)
        return response.json["api_key"]

    def headers(self, key):
        return {"X-API-KEY": key}

    def test_credentials_are_validated_and_keys_are_hashed(self):
        self.assertEqual(self.client.post("/auth/register", json={}).status_code, 400)
        key = self.register("alice")
        user = User.query.filter_by(email="alice@example.com").one()
        self.assertNotEqual(user.api_key_hash, key)
        self.assertEqual(user.api_key_hash, hashlib.sha256(key.encode()).hexdigest())
        self.assertEqual(self.client.post("/auth/register", json={
            "email": "alice@example.com", "password": "test-pass-123"
        }).status_code, 409)
        self.assertEqual(self.client.get("/indicators/").status_code, 401)
        self.assertEqual(self.client.get("/indicators/", headers=self.headers("bad")).status_code, 403)
        self.assertEqual(self.client.get("/indicators/", headers=self.headers(key)).status_code, 200)

    def test_login_rotates_api_key(self):
        old = self.register("alice")
        response = self.client.post("/auth/login", json={
            "email": "alice@example.com", "password": "test-pass-123"
        })
        self.assertEqual(response.status_code, 200)
        new = response.json["api_key"]
        self.assertNotEqual(new, old)
        self.assertEqual(self.client.get("/indicators/", headers=self.headers(old)).status_code, 403)
        self.assertEqual(self.client.get("/indicators/", headers=self.headers(new)).status_code, 200)
        self.assertEqual(self.client.post("/auth/login", json={
            "email": "alice@example.com", "password": "wrong-password"
        }).status_code, 401)

    def test_users_cannot_read_or_mutate_each_others_records(self):
        alice = self.register("alice")
        bob = self.register("bob")
        response = self.client.post("/indicators/", headers=self.headers(alice),
                                    json={"code": "NY.GDP.MKTP.CD", "name": "GDP"})
        self.assertEqual(response.status_code, 201)
        indicator_id = response.json["id"]
        response = self.client.get("/indicators/", headers=self.headers(bob))
        self.assertEqual(response.json, [])

        snapshot = {
            "indicator_id": indicator_id,
            "country": "GB",
            "year": 2023,
            "value": 2.4,
        }
        self.assertEqual(self.client.post("/snapshots/", headers=self.headers(bob),
                                          json=snapshot).status_code, 404)
        response = self.client.post("/snapshots/", headers=self.headers(alice),
                                    json=snapshot)
        self.assertEqual(response.status_code, 201)
        snap_id = response.json["id"]
        url = f"/snapshots/{snap_id}"
        self.assertEqual(self.client.get("/snapshots/", headers=self.headers(bob)).json, [])
        self.assertEqual(self.client.get(url, headers=self.headers(bob)).status_code, 404)
        self.assertEqual(self.client.put(url, headers=self.headers(bob),
                                         json={"value": 1.0}).status_code, 404)
        self.assertEqual(self.client.delete(url, headers=self.headers(bob)).status_code, 404)
        self.assertEqual(self.client.get(url, headers=self.headers(alice)).status_code, 200)
        self.assertEqual(self.client.delete(url, headers=self.headers(alice)).status_code, 200)


if __name__ == "__main__":
    unittest.main()
