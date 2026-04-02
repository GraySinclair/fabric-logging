import uuid
import json
import logging
from datetime import datetime, timezone

import notebookutils


class JsonLineFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        payload = {
            "ts": datetime.fromtimestamp(record.created, tz=timezone.utc).strftime("%Y-%m-%d %H:%M:%S.%f")[:-3],
            "level": record.levelname,
            "logger": record.name,
            "msg": record.getMessage(),
            "context": getattr(record, "context", {}),
        }
        return json.dumps(payload, ensure_ascii=False)


class LakehouseJsonlHandler(logging.Handler):
    def __init__(self, file_path: str):
        super().__init__()
        self.file_path = file_path

    def emit(self, record: logging.LogRecord) -> None:
        try:
            line = self.format(record) + "\n"
            notebookutils.fs.append(self.file_path, line, True)
        except Exception:
            self.handleError(record)


def build_logger(name: str, level: int = logging.INFO) -> logging.Logger:
    logger = logging.getLogger(name)
    logger.handlers.clear()
    logger.propagate = False
    logger.setLevel(level)

    log_path = f"Files/logs/{name}/{uuid.uuid4().hex}.json"
    logger.addHandler(logging.StreamHandler())
    logger.addHandler(LakehouseJsonlHandler(log_path))

    formatter = JsonLineFormatter()
    for h in logger.handlers:
        h.setFormatter(formatter)

    return logger