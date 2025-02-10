from http import HTTPStatus

import django.test

from lyceum.middleware import ReverseRussianWordsMiddleware
from lyceum.settings import ALLOW_REVERSE


class TestStaticURL(django.test.TestCase):
    def setUp(self):
        ReverseRussianWordsMiddleware.response_count = 0

    def test_default_catalog_endpoint(self):
        client = django.test.Client()
        for i in range(1, 21):
            response = client.get("/catalog/")
            word = "Список элементов"
            if i % 10 == 0 and ALLOW_REVERSE:
                # Переворачиваем каждое слово
                word = " ".join(i[::-1] for i in word.split())

            self.assertEqual(response.status_code, HTTPStatus.OK)
            self.assertEqual(
                response.content.decode("utf-8"),
                "<body>" + word + "</body>",
            )

    def test_catalog_with_index_endpoint(self):
        client = django.test.Client()
        for i in range(1, 21):
            response = client.get("/catalog/1/")
            word = "Подробно элемент"
            if i % 10 == 0 and ALLOW_REVERSE:
                # Переворачиваем каждое слово
                word = " ".join(i[::-1] for i in word.split())

            self.assertEqual(response.status_code, HTTPStatus.OK)
            self.assertEqual(
                response.content.decode("utf-8"),
                "<body>" + word + "</body>",
            )

    def test_valid_regex_positive_number(self):
        response = self.client.get("/catalog/re/123/")
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.content.decode("utf-8"), "123")

    def test_valid_converter_to_posint(self):
        response = self.client.get("/catalog/converter/123/")
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.content.decode("utf-8"), "123")
