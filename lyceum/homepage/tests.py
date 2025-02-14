from http import HTTPStatus

from django.test import Client, TestCase

from lyceum.middleware import ReverseRussianWordsMiddleware


class TestStaticURL(TestCase):
    def setUp(self):
        ReverseRussianWordsMiddleware.response_count = 0

    def test_homepage_endpoint_status(self):
        client = Client()

        response = client.get("/")

        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_homepage_endpoint_content(self):
        client = Client()

        response = client.get("/")
        word = "Главная"

        self.assertEqual(
            response.content.decode("utf-8"), "<body>" + word + "</body>"
        )

    def test_homepage_coffee_endpoint_status(self):
        client = Client()

        response = client.get("/coffee/")

        self.assertEqual(response.status_code, HTTPStatus.IM_A_TEAPOT)

    def test_homepage_coffee_endpoint_content(self):
        client = Client()

        response = client.get("/coffee/")
        word = "Я чайник"

        self.assertEqual(response.content.decode("utf-8"), word)
