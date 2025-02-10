import re

from .settings import ALLOW_REVERSE


class ReverseRussianWordsMiddleware:
    response_count = 0

    def __init__(self, get_response):
        self.get_response = get_response
        self.allow_reverse = ALLOW_REVERSE

    def __call__(self, request):
        response = self.get_response(request)
        ReverseRussianWordsMiddleware.response_count += 1

        if self.allow_reverse and (
            ReverseRussianWordsMiddleware.response_count % 10 == 0
        ):
            content_type = response.get("Content-Type", "")
            if "text" in content_type or content_type == "":
                content = response.content.decode("utf-8")
                pattern = r"([а-яА-ЯёЁ]+)"

                def reverse_russian(match):
                    word = match.group(0)
                    return word[::-1]

                new_content = re.sub(pattern, reverse_russian, content)
                response.content = new_content.encode("utf-8")
        return response
