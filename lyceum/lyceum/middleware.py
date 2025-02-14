import re


class ReverseRussianWordsMiddleware:
    response_count = 0

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        from django.conf import settings

        response = self.get_response(request)
        ReverseRussianWordsMiddleware.response_count += 1
        remainder = ReverseRussianWordsMiddleware.response_count % 10
        if settings.ALLOW_REVERSE and remainder == 0:
            self._reverse_content(response)

        return response

    def _reverse_content(self, response):
        content_type = response.get("Content-Type", "")
        if "text" in content_type or content_type == "":
            content = response.content.decode()

            reversed_content = re.sub(
                r"\b[а-яА-ЯёЁ]+\b",
                lambda m: m.group(0)[::-1],
                content,
            )
            response.content = reversed_content.encode()
