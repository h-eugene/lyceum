import re

from transliterate import translit


def normalize_name(name):
    if not name:
        return ""
    name = name.lower()
    normalized = translit(name, "ru", reversed=True)
    name = re.sub(r"[^a-z0-9-]", "", normalized.strip())
    return name


__all__ = []
