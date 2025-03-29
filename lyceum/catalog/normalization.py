import re

from transliterate import translit


def normalize_name(name):
    if not name:
        return ""
    normalized = translit(name.lower().strip(), "ru", reversed=True)
    return re.sub(r"[^a-z0-9-а-я]", "", normalized)


__all__ = []
