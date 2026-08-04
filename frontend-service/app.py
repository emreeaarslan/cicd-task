import os

import requests
from flask import Flask, render_template

app = Flask(__name__)

BACKEND_URL = os.getenv("BACKEND_URL", "http://127.0.0.1:5001")


@app.get("/")
def index():
    """Render the frontend home page."""
    return render_template("index.html")


@app.get("/message")
def get_backend_message():
    """Request a message from the backend service and render it."""
    try:
        response = requests.get(
            f"{BACKEND_URL}/api/message",
            timeout=3,
        )
        response.raise_for_status()

        data = response.json()
        message = data["message"]

        return render_template(
            "index.html",
            message=message,
        )

    except (requests.RequestException, KeyError, ValueError):
        return render_template(
            "index.html",
            error="Backend service is currently unavailable.",
        ), 502


@app.get("/health")
def health():
    """Return the current health status of the frontend service."""
    return {
        "service": "frontend",
        "status": "ok",
    }, 200


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5002,
        debug=False,
    )