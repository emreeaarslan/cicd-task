import os
import time

import requests
from flask import Flask, Response, g, render_template, request
from prometheus_client import CONTENT_TYPE_LATEST, generate_latest

from logging_config import configure_logger
from metrics_config import (
    HTTP_REQUEST_DURATION_SECONDS,
    HTTP_REQUESTS_TOTAL,
)
from telemetry_config import configure_tracing

app = Flask(__name__)

configure_tracing(app)
logger = configure_logger("frontend")

BACKEND_URL = os.getenv("BACKEND_URL", "http://127.0.0.1:5001")


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


@app.get("/metrics")
def metrics():
    """Expose Prometheus metrics."""
    return Response(
        generate_latest(),
        content_type=CONTENT_TYPE_LATEST,
    )


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5002,
        debug=False,
    )