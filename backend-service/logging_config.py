import json
import logging
import sys
from datetime import datetime, timezone


class JsonFormatter(logging.Formatter):
    def __init__(self, service):
        super().__init__()
        self.service = service

    def format(self, record):
        log_record = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "level": record.levelname,
            "service": self.service,
            "message": record.getMessage(),
        }

        for field in ("method", "path", "status", "duration_ms"):
            value = getattr(record, field, None)
            if value is not None:
                log_record[field] = value

        return json.dumps(log_record)


def configure_logger(service):
    logger = logging.getLogger(service)
    logger.setLevel(logging.INFO)
    logger.handlers.clear()
    logger.propagate = False

    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(JsonFormatter(service))

    logger.addHandler(handler)
    return logger
