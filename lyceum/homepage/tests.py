from http import HTTPStatus

import django.test

from lyceum.middleware import ReverseRussianWordsMiddleware
from lyceum.settings import get_allow_reverse
from unittest.mock import patch

import os


class TestStaticURL(django.test.TestCase):
    def setUp(self):
        ReverseRussianWordsMiddleware.response_count = 0

    def test_homepage_endpoint(self):
        client = django.test.Client()

        for i in range(1, 21):
            response = client.get("/")
            word = "Главная"
            if i % 10 == 0 and get_allow_reverse():
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
            if i % 10 == 0 and get_allow_reverse():
                # Переворачиваем каждое слово
                word = " ".join(i[::-1] for i in word.split())

            self.assertEqual(response.status_code, HTTPStatus.IM_A_TEAPOT)
            self.assertEqual(response.content.decode("utf-8"), word)

    def test_homepage_coffee(self):
        client2 = django.test.Client()
        client = django.test.Client()

        with patch.dict(os.environ, {"DJANGO_ALLOW_REVERSE": "True"}):
            for i in range(1, 21):
                response = client.get("/coffee/")
                response2 = client2.get("/coffee/")
                word = "Я чайник"
                word2 = word
                if i % 5 == 0 and get_allow_reverse():
                    word2 = " ".join(i[::-1] for i in word.split())
                self.assertEqual(response.status_code, HTTPStatus.IM_A_TEAPOT)
                self.assertEqual(response.content.decode(), word)
                self.assertEqual(response2.status_code, HTTPStatus.IM_A_TEAPOT)
                self.assertEqual(response2.content.decode(), word2)

        with patch.dict(os.environ, {"DJANGO_ALLOW_REVERSE": "False"}):

            for i in range(1, 21):
                response = client.get("/coffee/")
                word = "Я чайник"
                self.assertEqual(response.status_code, HTTPStatus.IM_A_TEAPOT)
                self.assertEqual(response.content.decode("utf-8"), word)
                self.assertNotIn("Я кинйач".encode(), response.content)
