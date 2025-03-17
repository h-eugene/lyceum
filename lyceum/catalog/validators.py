import re

from django.core.exceptions import ValidationError


class ValidateMustContain:
    def __init__(self, *required_words):
        if not required_words:
            raise ValueError(
                "Должно быть указано хотя бы одно обязательное слово.",
            )
        self.required_words = required_words

    def __call__(self, value):
        value_lower = value.lower()
        middle_part = "|".join(
            re.escape(word.lower()) for word in self.required_words
        )
        word_pattern = r"\b(" + middle_part + r")\b"
        if not re.search(word_pattern, value_lower):
            raise ValidationError(
                "Текст должен содержать хотя бы одно из слов: "
                f"{', '.join(self.required_words)}.",
            )

    def deconstruct(self):
        return (
            "catalog.validators.ValidateMustContain",
            self.required_words,
            {},
        )


def validate_slug(value):
    if not re.match(
        r"^[a-zA-Z0-9-_]+$",
        value,
    ):
        raise ValidationError(
            "Слаг может содержать только буквы, цифры, '-' и '_'",
        )


__all__ = ["ValidateMustContain"]
