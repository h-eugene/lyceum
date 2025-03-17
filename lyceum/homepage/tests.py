from http import HTTPStatus

from django.test import Client, TestCase
from django.urls import reverse

from lyceum.middleware import ReverseRussianWordsMiddleware


class TestStaticURL(TestCase):
    def setUp(self):
        super().setUp()
        ReverseRussianWordsMiddleware.response_count = 0

    def tearDown(self):
        super().tearDown()

    def test_homepage_endpoint_status(self):
        client = Client()

        response = client.get("/")

        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_homepage_coffee_endpoint_status(self):
        client = Client()
        url = reverse("homepage:coffee")
        response = client.get(url)

        self.assertEqual(response.status_code, HTTPStatus.IM_A_TEAPOT)

    def test_homepage_coffee_endpoint_content(self):
        client = Client()

        url = reverse("homepage:coffee")
        response = client.get(url)
        text = "Я чайник"

        self.assertEqual(response.content.decode("utf-8"), text)


__all__ = ["TestStaticURL"]
