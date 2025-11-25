import hashlib


def md5_hash(content: str) -> str:
    """Returns the MD5 digest (hex) of the given string."""

    return hashlib.md5(content.encode("utf-8")).hexdigest()
