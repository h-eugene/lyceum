from http import HTTPStatus

import django.test

from lyceum.middleware import ReverseRussianWordsMiddleware

from django.conf import settings


class TestStaticURL(django.test.TestCase):
    def setUp(self):
        ReverseRussianWordsMiddleware.response_count = 0

    def test_about_endpoint(self):
        client = django.test.Client()
        for i in range(1, 21):
            response = client.get("/about/")
            word = "О проекте"
            if i % 10 == 0 and settings.ALLOW_REVERSE:
                # Переворачиваем каждое слово
                word = " ".join(i[::-1] for i in word.split())

            self.assertEqual(response.status_code, HTTPStatus.OK)
            self.assertEqual(
                response.content.decode("utf-8"),
                "<body>" + word + "</body>",
            )
