import os
from pathlib import Path


bind = os.getenv("GUNICORN_BIND", "127.0.0.1:8001")
workers = int(os.getenv("GUNICORN_WORKERS", "3"))
worker_class = os.getenv(
    "GUNICORN_WORKER_CLASS",
    "deploy.gunicorn_worker.KiadezUvicornWorker",
)
accesslog = "-"
errorlog = "-"
capture_output = True
loglevel = os.getenv("GUNICORN_LOG_LEVEL", "info")
timeout = int(os.getenv("GUNICORN_TIMEOUT", "60"))
graceful_timeout = int(os.getenv("GUNICORN_GRACEFUL_TIMEOUT", "30"))
keepalive = int(os.getenv("GUNICORN_KEEPALIVE", "5"))
max_requests = int(os.getenv("GUNICORN_MAX_REQUESTS", "2000"))
max_requests_jitter = int(os.getenv("GUNICORN_MAX_REQUESTS_JITTER", "200"))
preload_app = False

if Path("/dev/shm").exists():
    worker_tmp_dir = "/dev/shm"

