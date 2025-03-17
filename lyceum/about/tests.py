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

    def test_about_endpoint_status(self):
        client = Client()
        url = reverse("about:about")
        response = client.get(url)

        self.assertEqual(response.status_code, HTTPStatus.OK)


__all__ = ["TestStaticURL"]
