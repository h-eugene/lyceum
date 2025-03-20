import re

from transliterate import translit


def normalize_name(name):
    if not name:
        return ""
    normalized = translit(name.lower(), "ru", reversed=True)
    return re.sub(r"[^a-z0-9-]", "", normalized.strip())


__all__ = []
