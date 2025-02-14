from http import HTTPStatus

import django.test

from lyceum.middleware import ReverseRussianWordsMiddleware


class TestStaticURL(django.test.TestCase):
    def setUp(self):
        ReverseRussianWordsMiddleware.response_count = 0

    def test_homepage_endpoint_status(self):
        client = django.test.Client()

        response = client.get("/")

        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_homepage_endpoint_content(self):
        client = django.test.Client()

        response = client.get("/")
        word = "Главная"

        self.assertEqual(
            response.content.decode("utf-8"), "<body>" + word + "</body>"
        )

    def test_homepage_coffee_endpoint_status(self):
        client = django.test.Client()

        response = client.get("/coffee/")

        self.assertEqual(response.status_code, HTTPStatus.IM_A_TEAPOT)

    def test_homepage_coffee_endpoint_content(self):
        client = django.test.Client()

        response = client.get("/coffee/")
        word = "Я чайник"

        self.assertEqual(response.content.decode("utf-8"), word)
