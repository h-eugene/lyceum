from http import HTTPStatus
from unittest.mock import patch

from django.conf import settings
import django.test

from lyceum.middleware import ReverseRussianWordsMiddleware


class TestStaticURL(django.test.TestCase):
    def setUp(self):
        ReverseRussianWordsMiddleware.response_count = 0

    def test_homepage_endpoint(self):
        client = django.test.Client()

        for i in range(1, 21):
            response = client.get("/")
            word = "Главная"
            if i % 10 == 0 and settings.ALLOW_REVERSE:
                word = word[::-1]

            self.assertEqual(response.status_code, HTTPStatus.OK)
            self.assertEqual(
                response.content.decode("utf-8"), "<body>" + word + "</body>"
            )

    def test_homepage_coffee_endpoint(self):
        client = django.test.Client()

        for i in range(1, 21):
            response = client.get("/coffee/")
            word = "Я чайник"
            if i % 10 == 0 and settings.ALLOW_REVERSE:
                # Переворачиваем каждое слово
                word = " ".join(i[::-1] for i in word.split())

            self.assertEqual(response.status_code, HTTPStatus.IM_A_TEAPOT)
            self.assertEqual(response.content.decode("utf-8"), word)

    def test_homepage_coffee_endpoint_with_two_clients(self):
        client2 = django.test.Client()
        client = django.test.Client()

        with patch("django.conf.settings.ALLOW_REVERSE", True):
            for i in range(1, 21):
                response = client.get("/coffee/")
                response2 = client2.get("/coffee/")
                word = "Я чайник"
                word2 = word
                if i % 5 == 0 and settings.ALLOW_REVERSE:
                    word2 = " ".join(i[::-1] for i in word.split())
                self.assertEqual(response.content.decode(), word)
                self.assertEqual(response2.content.decode(), word2)

    def test_homepage_coffee_endpoint_with_reverse_disabled(self):
        client = django.test.Client()
        with patch("django.conf.settings.ALLOW_REVERSE", False):
            for i in range(1, 21):
                response = client.get("/coffee/")
                word = "Я чайник"
                self.assertEqual(response.status_code, HTTPStatus.IM_A_TEAPOT)
                self.assertEqual(response.content.decode("utf-8"), word)
