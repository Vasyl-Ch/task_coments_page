import bleach

ALLOWED_TAGS = {"a", "code", "i", "strong"}

ALLOWED_ATTRS = {
    "a": ["href", "title", "rel"],
}


def sanitize_text(raw_text: str) -> str:
    """
    clean HTML and safe from xss
    """
    cleaned = bleach.clean(
        raw_text, tags=ALLOWED_TAGS, attributes=ALLOWED_ATTRS, strip=True
    )
    return cleaned
