import os
import psycopg2
from flask import Flask, jsonify

# Lightweight Flask API demonstrating health/user endpoints backed by Postgres.
app = Flask(__name__)


def get_db_config():
    """
    Central place to read database settings so the rest of the code stays simple
    and the config is easily overridden via environment variables.
    """
    return {
        "host": os.getenv("DB_HOST", "postgres-service"),
        "dbname": os.getenv("DB_NAME", "usersdb"),
        "user": os.getenv("DB_USER", "appuser"),
        "password": os.getenv("DB_PASSWORD", "changeme"),
        "port": os.getenv("DB_PORT", "5432"),
    }


def get_connection():
    """Open a short-lived connection; context managers ensure cleanup."""
    return psycopg2.connect(**get_db_config())


def init_db():
    """
    Create table and seed data if empty. This keeps the demo deterministic for
    interviews and CI runs without needing a separate migration step.
    """
    with get_connection() as conn:
        with conn.cursor() as cur:
            # Schema creation is idempotent; safe to run on every start/request.
            cur.execute(
                """
                CREATE TABLE IF NOT EXISTS users (
                    id SERIAL PRIMARY KEY,
                    name TEXT NOT NULL,
                    email TEXT NOT NULL UNIQUE
                );
                """
            )
            cur.execute("SELECT COUNT(*) FROM users;")
            count = cur.fetchone()[0]
            if count == 0:
                # Seed predictable demo data so the frontend always has content.
                cur.executemany(
                    "INSERT INTO users (name, email) VALUES (%s, %s);",
                    [
                        ("Ada Lovelace", "ada@example.com"),
                        ("Grace Hopper", "grace@example.com"),
                        ("Alan Turing", "alan@example.com"),
                    ],
                )


@app.after_request
def add_cors_headers(response):
    """Allow local dev tools and the static site to call the API directly."""
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type"
    return response


@app.route("/health", methods=["GET"])
def health():
    """Basic liveness/readiness signal and DB reachability check."""
    status = {"status": "ok", "database": "unknown"}
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                # A trivial query is enough to validate DB connectivity.
                cur.execute("SELECT 1;")
                cur.fetchone()
                status["database"] = "reachable"
    except Exception as exc:  # pylint: disable=broad-except
        status["database"] = f"error: {exc}"
    return jsonify(status)


@app.route("/users", methods=["GET"])
@app.route("/api/users", methods=["GET"])  # Keep compatibility with /api prefix behind nginx/ingress.
def list_users():
    """Return all users as JSON; seeds the DB on first request for reliability."""
    try:
        init_db()
        with get_connection() as conn:
            with conn.cursor() as cur:
                # Order by id for a stable, deterministic response body.
                cur.execute("SELECT id, name, email FROM users ORDER BY id;")
                rows = cur.fetchall()
                users = [
                    {"id": row[0], "name": row[1], "email": row[2]} for row in rows
                ]
                return jsonify({"users": users})
    except Exception as exc:  # pylint: disable=broad-except
        return jsonify({"error": str(exc)}), 500


if __name__ == "__main__":
    # Flask dev server for local use; in containers we run via gunicorn.
    app.run(host="0.0.0.0", port=5000)

