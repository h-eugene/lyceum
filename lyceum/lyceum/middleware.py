import re


class ReverseRussianWordsMiddleware:
    response_count = 0

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        from .settings import get_allow_reverse

        response = self.get_response(request)
        ReverseRussianWordsMiddleware.response_count += 1

        if (
            get_allow_reverse()
            and ReverseRussianWordsMiddleware.response_count % 10 == 0
        ):
            self._reverse_content(response)

        return response

    def _reverse_content(self, response):
        content_type = response.get("Content-Type", "")
        if "text" in content_type or content_type == "":
            content = response.content.decode("utf-8")

            reversed_content = re.sub(
                r"\b[а-яА-ЯёЁ]+\b",
                lambda m: m.group(0)[::-1],
                content,
            )
            response.content = reversed_content.encode("utf-8")
