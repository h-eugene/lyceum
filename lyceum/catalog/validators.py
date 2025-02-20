import re

from django.core.exceptions import ValidationError


def has_prevoshodno_or_roskoshno_word(value):
    if not ("превосходно" in value or "роскошно" in value):
        raise ValidationError(
            "Текст должен содержать слово 'превосходно' или 'роскошно'."
        )


def validate_weight(value):
    if value > 32767 or value < 1:
        raise ValidationError("Вес должен быть от 1 до 32767.")


def validate_slug(value):
    if not re.match(r"^[a-zA-Z0-9-_]+$", value):
        raise ValidationError(
            "Слаг может содержать только буквы, цифры, '-' и '_'"
        )
