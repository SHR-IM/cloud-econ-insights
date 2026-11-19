# Cloud Economics Insights API

An **academic Python/Flask REST API prototype** for retrieving and storing economic indicators. Developed for the ECS781P Cloud Computing module at Queen Mary University of London.

This repository demonstrates a small backend service, rather than a production deployment. It integrates with the World Bank API, uses Flask-SQLAlchemy for relational persistence, and supports per-user API keys.

## Stack

Python 3.11, Flask, Flask-SQLAlchemy, SQLite for local development (PostgreSQL may be configured using DATABASE_URL), requests, Docker and Gunicorn.

## Capabilities

- Register and log in via POST /auth/register and POST /auth/login.
- Create and list your own economic indicators via /indicators/.
- Create, list, retrieve, update and delete your own economic snapshots via /snapshots/.
- Explore integration code for querying World Bank economic data in external_api.py.
- API key authentication using the X-API-KEY request header.

**Important scope note:** The World Bank fetching helper exists in the codebase; these routes do not automatically sync data from that service. This is a learning project, not a live cloud service or a security-audited production API.

## Run locally

1. Create and activate a Python 3.11+ virtual environment.
2. Run: pip install -r requirements.txt
3. Start the server: python app.py
4. Visit http://127.0.0.1:8080/

The default database is a local SQLite file; set DATABASE_URL for a different database.

Example registration:

    curl -X POST http://127.0.0.1:8080/auth/register \
      -H "Content-Type: application/json" \
      -d '{"email":"demo@example.com","password":"change-this-password"}'

The response contains a newly issued API key. Provide that value in an X-API-KEY header to use protected endpoints. Logging in issues a **new** API key and revokes the previous one.

## Test

    python -m unittest discover -s tests -v

Tests check input validation, API key hashing and rotation, and data isolation between two users. These are regression tests, not a penetration test or assurance of production readiness.

## Security and repository hygiene

- Passwords use Werkzeug's password hashing utilities.
- Newly issued API keys are high-entropy random values, stored only as SHA-256 hashes.
- Protected queries are scoped to the authenticated user.
- Local databases, virtual environments and Python caches are excluded by .gitignore and .dockerignore.
- The former repository version committed a database and development files. **Removing files from the current branch does not erase them from Git history.** If real credentials or private data were present, revoke/rotate affected credentials and carefully review the history before publicizing this repository further.
- Existing plaintext API keys in a previously created database cannot authenticate using the new code. For a disposable coursework database, recreate it; otherwise arrange a migration and key reset. Do not discard valuable user data.

## Limitations and next steps

For a real deployment, add database migrations, better API input schemas, rate limits, secret management, TLS termination, dependency pinning/scanning, CI, and integration tests against the deployed environment. The project does not claim these production controls already exist.

## Repository layout

- app.py and config.py: Flask application factory and configuration
- models.py: users, economic indicators and historical snapshots
- auth.py: API-key handling
- routes/: HTTP endpoints
- external_api.py: World Bank request helper
- tests/: local regression tests
- Dockerfile: container build for the academic service

*Portfolio update, November 2026: security hardening and presentation cleanup of the original university coursework.*
