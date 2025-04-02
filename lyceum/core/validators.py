import re

from django.core.exceptions import ValidationError


def validate_slug(value):
    if not re.match(
        r"^[a-zA-Z0-9-_]+$",
        value,
    ):
        raise ValidationError(
            "Слаг может содержать только буквы, цифры, '-' и '_'",
        )


__all__ = []
