#!/usr/bin/env python3
"""
Configure CORS rules on the configured S3 bucket (Backblaze B2 S3 compatible).

Why:
- Browser uploads to a presigned PUT URL require the bucket to answer the CORS preflight.
- Without a bucket CORS rule, uploads from http://localhost:5173 will fail with "CORS request did not succeed".

Usage:
  ./venv/bin/python scripts/apply_media_bucket_cors.py --show
  ./venv/bin/python scripts/apply_media_bucket_cors.py --apply
  ./venv/bin/python scripts/apply_media_bucket_cors.py --apply --origins http://localhost:5173,http://127.0.0.1:5173
"""

from __future__ import annotations

import argparse
import base64
import json
import os
import sys
from pathlib import Path
from typing import List
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

from botocore.exceptions import ClientError

# Allow running as a script (python scripts/...) without requiring PYTHONPATH.
# When executed this way, Python sets sys.path[0] to "scripts/", which would
# otherwise prevent imports like "from app..." from resolving.
PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from app.core.config import settings
from app.core.storage import ensure_s3_configured, get_s3_client


def _normalize_origin(origin: str) -> str:
    origin = (origin or "").strip()
    while origin.endswith("/"):
        origin = origin[:-1]
    return origin


def _default_origins() -> List[str]:
    origins: list[str] = []
    raw = settings.CORS_ALLOW_ORIGINS or ""
    for part in raw.split(","):
        value = _normalize_origin(part)
        if value:
            origins.append(value)

    # Ensure the frontend URL is always included (used in emails and often in deployments).
    frontend = _normalize_origin(settings.FRONTEND_URL or "")
    if frontend:
        origins.append(frontend)

    # Common local dev variants.
    origins.extend(
        [
            "http://localhost:5173",
            "http://127.0.0.1:5173",
            "http://localhost:3000",
            "http://127.0.0.1:3000",
        ]
    )

    # Keep stable order but dedupe.
    seen = set()
    normalized: list[str] = []
    for origin in origins:
        if origin in seen:
            continue
        seen.add(origin)
        normalized.append(origin)
    return normalized


def _desired_cors_configuration(origins: List[str]) -> dict:
    return {
        "CORSRules": [
            {
                "AllowedOrigins": origins,
                "AllowedMethods": ["GET", "PUT", "POST", "HEAD"],
                "AllowedHeaders": ["*"],
                "ExposeHeaders": ["ETag"],
                "MaxAgeSeconds": 3000,
            }
        ]
    }


def _b2_api_versions_to_try() -> list[int]:
    # Backblaze B2 Native API current version is v4, but keep fallbacks.
    return [4, 3, 2]


def _http_json(*, method: str, url: str, headers: dict, body: dict | None = None) -> dict:
    data = None
    req_headers = dict(headers or {})
    if body is not None:
        data = json.dumps(body, ensure_ascii=True).encode("utf-8")
        req_headers.setdefault("Content-Type", "application/json")
    req = Request(url, data=data, method=method.upper(), headers=req_headers)
    try:
        with urlopen(req, timeout=30) as resp:
            raw = resp.read()
    except HTTPError as exc:
        raw = exc.read() if hasattr(exc, "read") else b""
        message = raw.decode("utf-8", errors="replace").strip()
        raise RuntimeError(f"B2 API HTTPError {exc.code} for {url}: {message}") from exc
    except URLError as exc:
        raise RuntimeError(f"B2 API connection error for {url}: {exc}") from exc

    if not raw:
        return {}
    return json.loads(raw.decode("utf-8"))


def _b2_authorize_account(*, key_id: str, application_key: str) -> dict:
    basic = base64.b64encode(f"{key_id}:{application_key}".encode("utf-8")).decode("ascii")
    headers = {"Authorization": f"Basic {basic}"}
    last_err: Exception | None = None
    for version in _b2_api_versions_to_try():
        url = f"https://api.backblazeb2.com/b2api/v{version}/b2_authorize_account"
        try:
            return _http_json(method="GET", url=url, headers=headers)
        except RuntimeError as exc:
            if "HTTPError 404" in str(exc):
                last_err = exc
                continue
            raise
    raise RuntimeError("Could not authorize with Backblaze B2. Last error: " + str(last_err))


def _b2_list_buckets(*, api_url: str, token: str, account_id: str, bucket_name: str) -> dict:
    headers = {"Authorization": token}
    # Per docs, using an app key restricted to a bucket requires specifying bucketName/bucketId.
    body = {"accountId": account_id, "bucketName": bucket_name}
    last_err: Exception | None = None
    for version in _b2_api_versions_to_try():
        url = f"{api_url}/b2api/v{version}/b2_list_buckets"
        try:
            return _http_json(method="POST", url=url, headers=headers, body=body)
        except RuntimeError as exc:
            if "HTTPError 404" in str(exc):
                last_err = exc
                continue
            raise
    raise RuntimeError("Could not list buckets via Backblaze B2. Last error: " + str(last_err))


def _b2_update_bucket(*, api_url: str, token: str, account_id: str, bucket_id: str, cors_rules: list[dict]) -> dict:
    headers = {"Authorization": token}
    body = {"accountId": account_id, "bucketId": bucket_id, "corsRules": cors_rules}
    last_err: Exception | None = None
    for version in _b2_api_versions_to_try():
        url = f"{api_url}/b2api/v{version}/b2_update_bucket"
        try:
            return _http_json(method="POST", url=url, headers=headers, body=body)
        except RuntimeError as exc:
            if "HTTPError 404" in str(exc):
                last_err = exc
                continue
            raise
    raise RuntimeError("Could not update bucket via Backblaze B2. Last error: " + str(last_err))


def _desired_b2_cors_rule(*, origins: list[str]) -> dict:
    # Backblaze B2 CORS uses "allowedOperations". For S3-compatible operations,
    # Backblaze expects lowercase identifiers like "s3_put" (case-sensitive).
    return {
        "corsRuleName": "kiadez-s3-cors",
        "allowedOrigins": origins,
        "allowedHeaders": ["*"],
        "allowedOperations": ["s3_get", "s3_head", "s3_put"],
        "exposeHeaders": ["ETag"],
        "maxAgeSeconds": 3600,
    }


def _get_bucket_cors(client, bucket: str) -> dict | None:
    try:
        return client.get_bucket_cors(Bucket=bucket)
    except ClientError as exc:
        code = (exc.response or {}).get("Error", {}).get("Code")
        if code in {"NoSuchCORSConfiguration", "NoSuchCorsConfiguration"}:
            return None
        raise


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--show",
        action="store_true",
        help="Print current bucket CORS configuration (if any) and exit.",
    )
    parser.add_argument(
        "--apply",
        action="store_true",
        help="Apply the recommended CORS configuration to the bucket.",
    )
    parser.add_argument(
        "--bucket-id",
        default="",
        help="Backblaze B2 bucketId override (only needed if the app key cannot list buckets).",
    )
    parser.add_argument(
        "--origins",
        default="",
        help="Comma-separated allowed origins override. If omitted, uses backend settings + common localhost origins.",
    )
    args = parser.parse_args()

    ensure_s3_configured()
    client = get_s3_client()
    bucket = settings.S3_BUCKET or ""

    current = _get_bucket_cors(client, bucket)
    if args.show:
        # Show both S3-compatible CORS (get_bucket_cors) and B2 Native CORS rules (b2_list_buckets).
        result: dict = {"s3_compatible_api": current or {"CORSRules": []}}
        try:
            b2_key_id = (os.environ.get("B2_APPLICATION_KEY_ID") or "").strip() or (settings.S3_ACCESS_KEY_ID or "")
            b2_app_key = (os.environ.get("B2_APPLICATION_KEY") or "").strip() or (settings.S3_SECRET_ACCESS_KEY or "")
            if b2_key_id and b2_app_key:
                auth = _b2_authorize_account(key_id=b2_key_id, application_key=b2_app_key)
                api_url = (
                    auth.get("apiUrl")
                    or (((auth.get("apiInfo") or {}).get("storageApi") or {}).get("apiUrl"))
                    or ""
                )
                token = auth.get("authorizationToken") or ""
                account_id = auth.get("accountId") or ""
                if api_url and token and account_id:
                    buckets = (
                        _b2_list_buckets(api_url=api_url, token=token, account_id=account_id, bucket_name=bucket).get("buckets")
                        or []
                    )
                    bucket_obj = buckets[0] if buckets else {}
                    result["b2_native_api"] = {
                        "bucketId": bucket_obj.get("bucketId") or "",
                        "corsRules": bucket_obj.get("corsRules") or [],
                    }
        except Exception as exc:
            result["b2_native_api"] = {"error": str(exc)}

        print(json.dumps(result, indent=2, ensure_ascii=True))
        return 0

    if not args.apply:
        parser.error("Choose one: --show or --apply")

    if args.origins.strip():
        origins = [_normalize_origin(value) for value in args.origins.split(",") if _normalize_origin(value)]
    else:
        origins = _default_origins()

    desired = _desired_cors_configuration(origins)
    try:
        client.put_bucket_cors(Bucket=bucket, CORSConfiguration=desired)
        print("Applied bucket CORS configuration (S3 PutBucketCors):")
        print(json.dumps(desired, indent=2, ensure_ascii=True))
        return 0
    except ClientError as exc:
        code = (exc.response or {}).get("Error", {}).get("Code", "")
        msg = (exc.response or {}).get("Error", {}).get("Message", "")
        if code == "InvalidRequest" and "B2 Native CORS rules" in msg:
            # Backblaze restriction: if the bucket has native CORS rules, you must update them
            # via the Native API (b2_update_bucket), not via S3 PutBucketCors.
            b2_key_id = (os.environ.get("B2_APPLICATION_KEY_ID") or "").strip() or (settings.S3_ACCESS_KEY_ID or "")
            b2_app_key = (os.environ.get("B2_APPLICATION_KEY") or "").strip() or (settings.S3_SECRET_ACCESS_KEY or "")
            if not b2_key_id or not b2_app_key:
                raise RuntimeError(
                    "Bucket has B2 Native CORS rules, but B2 credentials are missing. "
                    "Set env vars B2_APPLICATION_KEY_ID and B2_APPLICATION_KEY (or configure S3_* in .env)."
                ) from exc

            auth = _b2_authorize_account(key_id=b2_key_id, application_key=b2_app_key)
            api_url = (
                auth.get("apiUrl")
                or (((auth.get("apiInfo") or {}).get("storageApi") or {}).get("apiUrl"))
                or ""
            )
            token = auth.get("authorizationToken") or ""
            account_id = auth.get("accountId") or ""
            if not api_url or not token or not account_id:
                raise RuntimeError("Unexpected b2_authorize_account response; missing apiUrl/token/accountId.") from exc

            bucket_id = (args.bucket_id or "").strip()
            existing_rules: list[dict] = []
            if not bucket_id:
                buckets = (
                    _b2_list_buckets(api_url=api_url, token=token, account_id=account_id, bucket_name=bucket).get("buckets")
                    or []
                )
                if not buckets:
                    raise RuntimeError(f"Could not find bucket '{bucket}' via b2_list_buckets. Provide --bucket-id.") from exc
                bucket_obj = buckets[0]
                bucket_id = bucket_obj.get("bucketId") or ""
                existing_rules = bucket_obj.get("corsRules") or []
            if not bucket_id:
                raise RuntimeError("Missing bucketId; provide --bucket-id.") from exc

            desired_rule = _desired_b2_cors_rule(origins=origins)
            merged_rules = [
                rule for rule in (existing_rules or []) if rule.get("corsRuleName") != desired_rule["corsRuleName"]
            ]
            merged_rules.insert(0, desired_rule)

            updated = _b2_update_bucket(
                api_url=api_url,
                token=token,
                account_id=account_id,
                bucket_id=bucket_id,
                cors_rules=merged_rules,
            )

            print("Applied bucket CORS configuration via Backblaze B2 Native API (b2_update_bucket):")
            print(json.dumps(updated.get("corsRules") or merged_rules, indent=2, ensure_ascii=True))
            return 0

        raise


if __name__ == "__main__":
    raise SystemExit(main())
