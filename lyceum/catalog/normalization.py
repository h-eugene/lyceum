from transliterate import translit
import re


def normalize_name(name):
    if not name:
        return ""
    name = name.lower()
    normalized = translit(name, "ru", reversed=True)
    name = re.sub(r"[^a-z0-9-]", "", normalized.strip())
    return name
