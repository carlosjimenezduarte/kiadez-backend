from __future__ import annotations

from fastapi import Request


def normalize_locale(raw: str | None) -> str:
    value = (raw or "").strip().lower()
    if value.startswith("es"):
        return "es"
    if value.startswith("fr"):
        return "fr"
    return "en"


def locale_from_request(request: Request | None, default: str = "en") -> str:
    if request is None:
        return normalize_locale(default)
    header = (request.headers.get("accept-language") or "").strip()
    if not header:
        return normalize_locale(default)
    first = header.split(",")[0].split(";")[0].strip()
    if not first:
        return normalize_locale(default)
    return normalize_locale(first)


def tr(locale: str, *, es: str, en: str, fr: str | None = None) -> str:
    normalized = normalize_locale(locale)
    if normalized == "es":
        return es
    if normalized == "fr":
        return fr or en
    return en
