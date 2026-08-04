from flask import Flask, jsonify

app = Flask(__name__)


@app.get("/health")
def health():
    """Return the current health status of the backend service."""
    return jsonify(
        {
            "service": "backend",
            "status": "ok",
        }
    ), 200


@app.get("/api/message")
def get_message():
    """Return a sample message for the frontend service."""
    return jsonify(
        {
            "service": "backend",
            "message": "Backend service is working.",
        }
    ), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=False)