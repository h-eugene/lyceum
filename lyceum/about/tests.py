from http import HTTPStatus

from django.test import Client, TestCase
from django.urls import reverse


class TestStaticURL(TestCase):
    def test_about_endpoint_status(self):
        client = Client()
        url = reverse("about:about")
        response = client.get(url)

        self.assertEqual(response.status_code, HTTPStatus.OK)


__all__ = []
