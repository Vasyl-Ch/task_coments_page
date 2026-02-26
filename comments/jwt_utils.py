import jwt
from datetime import datetime, timedelta, UTC
from django.conf import settings


def create_token(user_name: str, email: str) -> str:
    now = datetime.now(UTC)
    payload = {
        "user_name": user_name,
        "email": email,
        "exp": now + timedelta(seconds=settings.JWT_EXP_DELTA_SECONDS),
        "iat": now,
    }
    return jwt.encode(payload, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)


def decode_token(token: str) -> dict | None:
    try:
        return jwt.decode(
            token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM]
        )
    except (jwt.ExpiredSignatureError, jwt.InvalidTokenError):
        return None
