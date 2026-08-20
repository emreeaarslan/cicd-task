import time

import psycopg
from flask import Flask, Response, g, jsonify, request
from prometheus_client import CONTENT_TYPE_LATEST, generate_latest

from db import check_database, get_latest_message, init_db, save_message
from logging_config import configure_logger
from metrics_config import (
    HTTP_REQUEST_DURATION_SECONDS,
    HTTP_REQUESTS_TOTAL,
)
from telemetry_config import configure_tracing

app = Flask(__name__)

configure_tracing(app)
logger = configure_logger("backend")

DEFAULT_MESSAGE = "Backend service is running"


@app.before_request
def start_request_timer():
    """Record the start time of each request."""
    g.request_started_at = time.perf_counter()


@app.after_request
def log_and_measure_request(response):
    """Write structured logs and record Prometheus request metrics."""
    duration_seconds = (
        time.perf_counter()
        - g.get("request_started_at", time.perf_counter())
    )
    duration_ms = duration_seconds * 1000
    endpoint = request.endpoint or "unknown"

    logger.info(
        "request completed",
        extra={
            "method": request.method,
            "path": request.path,
            "status": response.status_code,
            "duration_ms": round(duration_ms, 2),
        },
    )

    if request.path != "/metrics":
        HTTP_REQUESTS_TOTAL.labels(
            method=request.method,
            endpoint=endpoint,
            status=str(response.status_code),
        ).inc()

        HTTP_REQUEST_DURATION_SECONDS.labels(
            method=request.method,
            endpoint=endpoint,
        ).observe(duration_seconds)

    return response


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


@app.get("/metrics")
def metrics():
    """Expose Prometheus metrics."""
    return Response(
        generate_latest(),
        content_type=CONTENT_TYPE_LATEST,
    )


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
    app.run(
        host="0.0.0.0",
        port=5001,
        debug=False,
    )