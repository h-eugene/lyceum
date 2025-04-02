from http import HTTPStatus

from django.test import Client, TestCase
from django.urls import reverse


class TestStaticURL(TestCase):
    def test_default_catalog_endpoint_status(self):
        client = Client()
        url = reverse("catalog:item_list")
        response = client.get(url)

        self.assertEqual(response.status_code, HTTPStatus.OK)


__all__ = []
