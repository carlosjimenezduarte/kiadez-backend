import os

try:
    from uvicorn_worker import UvicornWorker
except ImportError:  # pragma: no cover - compatibility fallback
    from uvicorn.workers import UvicornWorker


class KiadezUvicornWorker(UvicornWorker):
    CONFIG_KWARGS = {
        **getattr(UvicornWorker, "CONFIG_KWARGS", {}),
        "proxy_headers": True,
        "forwarded_allow_ips": os.getenv("FORWARDED_ALLOW_IPS", "127.0.0.1"),
    }

