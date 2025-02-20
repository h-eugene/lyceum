from http import HTTPStatus

from django.test import Client, TestCase

from lyceum.middleware import ReverseRussianWordsMiddleware


class TestStaticURL(TestCase):
    def setUp(self):
        super().setUp()
        ReverseRussianWordsMiddleware.response_count = 0

    def test_homepage_endpoint_status(self):
        client = Client()

        response = client.get("/")

        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_homepage_endpoint_content(self):
        client = Client()

        response = client.get("/")
        text = "Главная"

        self.assertEqual(
            response.content.decode("utf-8"), "<body>" + text + "</body>"
        )

    def test_homepage_coffee_endpoint_status(self):
        client = Client()

        response = client.get("/coffee/")

        self.assertEqual(response.status_code, HTTPStatus.IM_A_TEAPOT)

    def test_homepage_coffee_endpoint_content(self):
        client = Client()

        response = client.get("/coffee/")
        text = "Я чайник"

        self.assertEqual(response.content.decode("utf-8"), text)
