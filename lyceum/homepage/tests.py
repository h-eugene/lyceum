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
        client = django.test.Client()

        with patch.dict(os.environ, {"DJANGO_ALLOW_REVERSE": "True"}):
            print(get_allow_reverse())
            for i in range(1, 21):
                response = client.get("/coffee/")
                word = "Я чайник"
                
                if i % 10 == 0 and get_allow_reverse():
                    word = " ".join(i[::-1] for i in word.split())
                self.assertEqual(response.status_code, HTTPStatus.IM_A_TEAPOT)
                self.assertEqual(response.content.decode("utf-8"), word)

        with patch.dict(os.environ, {"DJANGO_ALLOW_REVERSE": "False"}):
            print(get_allow_reverse())
            for i in range(1, 21):
                response = client.get("/coffee/")
                word = "Я чайник"
                self.assertEqual(response.status_code, HTTPStatus.IM_A_TEAPOT)
                self.assertEqual(response.content.decode("utf-8"), word)
                self.assertNotIn("Я кинйач".encode(), response.content)
