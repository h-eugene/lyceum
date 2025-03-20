import re

from django.conf import settings


class ReverseRussianWordsMiddleware:
    response_count = 0
    REVERSE_NUMBER = 10

    def should_reverse_response(self):
        return settings.ALLOW_REVERSE and (
            ReverseRussianWordsMiddleware.response_count == self.REVERSE_NUMBER
        )

    def __init__(self, get_response):
        self.get_response = get_response
        self.regex = re.compile(r"(?<!\w)[а-яА-ЯёЁ]+(?!\w)")

    def __call__(self, request):
        response = self.get_response(request)
        ReverseRussianWordsMiddleware.response_count += 1
        if self.should_reverse_response():
            ReverseRussianWordsMiddleware.response_count = 0
            self._reverse_content(response)

        return response

    def _reverse_content(self, response):
        content = response.content.decode()

        reversed_content = self.regex.sub(lambda m: m.group(0)[::-1], content)
        response.content = reversed_content.encode()


__all__ = []
