import psycopg
from flask import Flask, jsonify, request

from db import check_database, get_latest_message, init_db, save_message

app = Flask(__name__)

DEFAULT_MESSAGE = "Backend service is running - v1.0.2"


@app.get("/health")
def health():
    """Return the current health status of the backend service."""
    return jsonify(
        {
            "service": "backend",
            "status": "ok",
        }
    ), 200


@app.get("/health/ready")
def readiness():
    """Return whether the backend can reach PostgreSQL."""
    try:
        if check_database():
            return jsonify(
                {
                    "service": "backend",
                    "status": "ready",
                }
            ), 200

    except (psycopg.Error, RuntimeError):
        pass

    return jsonify(
        {
            "service": "backend",
            "status": "not ready",
        }
    ), 503


@app.get("/api/message")
def get_message():
    """Return the latest message stored in PostgreSQL."""
    init_db()

    message = get_latest_message()

    if message is None:
        save_message(DEFAULT_MESSAGE)
        message = DEFAULT_MESSAGE

    return jsonify(
        {
            "service": "backend",
            "message": message,
        }
    ), 200


@app.post("/api/message")
def create_message():
    """Store a new message in PostgreSQL."""
    data = request.get_json(silent=True) or {}
    message = data.get("message")

    if not isinstance(message, str) or not message.strip():
        return jsonify(
            {
                "service": "backend",
                "error": "message is required",
            }
        ), 400

    message = message.strip()

    init_db()
    save_message(message)

    return jsonify(
        {
            "service": "backend",
            "message": message,
        }
    ), 201


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=False)