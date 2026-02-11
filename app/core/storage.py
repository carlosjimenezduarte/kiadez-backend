from functools import lru_cache

import boto3
from botocore.config import Config

from app.core.config import settings


class S3NotConfiguredError(RuntimeError):
    pass


def ensure_s3_configured() -> None:
    required = {
        "S3_ENDPOINT": settings.S3_ENDPOINT,
        "S3_REGION": settings.S3_REGION,
        "S3_BUCKET": settings.S3_BUCKET,
        "S3_ACCESS_KEY_ID": settings.S3_ACCESS_KEY_ID,
        "S3_SECRET_ACCESS_KEY": settings.S3_SECRET_ACCESS_KEY,
    }
    missing = [key for key, value in required.items() if not value]
    if missing:
        raise S3NotConfiguredError(
            "S3 is not configured. Missing: " + ", ".join(missing)
        )


@lru_cache
def get_s3_client():
    ensure_s3_configured()
    addressing_style = "path" if settings.S3_FORCE_PATH_STYLE else "virtual"
    config = Config(
        signature_version="s3v4",
        s3={"addressing_style": addressing_style},
    )
    return boto3.client(
        "s3",
        aws_access_key_id=settings.S3_ACCESS_KEY_ID,
        aws_secret_access_key=settings.S3_SECRET_ACCESS_KEY,
        region_name=settings.S3_REGION,
        endpoint_url=settings.S3_ENDPOINT,
        config=config,
    )


def generate_presigned_put_url(*, key: str, content_type: str, expires_in: int) -> str:
    client = get_s3_client()
    return client.generate_presigned_url(
        "put_object",
        Params={
            "Bucket": settings.S3_BUCKET,
            "Key": key,
            "ContentType": content_type,
        },
        ExpiresIn=expires_in,
    )


def generate_presigned_get_url(*, key: str, expires_in: int) -> str:
    client = get_s3_client()
    return client.generate_presigned_url(
        "get_object",
        Params={
            "Bucket": settings.S3_BUCKET,
            "Key": key,
        },
        ExpiresIn=expires_in,
    )


def head_object(*, key: str) -> dict:
    client = get_s3_client()
    return client.head_object(
        Bucket=settings.S3_BUCKET,
        Key=key,
    )


def delete_object(*, key: str) -> None:
    client = get_s3_client()
    client.delete_object(
        Bucket=settings.S3_BUCKET,
        Key=key,
    )
