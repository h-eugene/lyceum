import re

from django.core.exceptions import ValidationError


class ValidateMustContain:
    def __init__(self, *required_words):
        self.required_words = required_words

    def __call__(self, value):
        value_lower = value.lower()
        if not any(
            word.lower() in value_lower for word in self.required_words
        ):
            raise ValidationError(
                "Текст должен содержать хотя бы одно из слов: "
                f"{', '.join(self.required_words)}."
            )

    def deconstruct(self):
        return (
            "catalog.validators.MustContainValidator",
            self.required_words,
            {},
        )


def validate_weight(value):
    if value > 32767 or value < 1:
        raise ValidationError("Вес должен быть от 1 до 32767.")


def validate_slug(value):
    if not re.match(
        r"^[a-zA-Z0-9-_]+$",
        value,
    ):
        raise ValidationError(
            "Слаг может содержать только буквы, цифры, '-' и '_'",
        )
