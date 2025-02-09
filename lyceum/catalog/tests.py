import django.test
from http import HTTPStatus


class TestStaticURL(django.test.TestCase):
    def test_default_catalog_endpoint(self):
        response = django.test.Client().get("/catalog/")
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_catalog_with_index_endpoint(self):
        response = django.test.Client().get("/catalog/1/")
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_valid_regex_positive_number(self):
        response = self.client.get("/catalog/re/123/")
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.content.decode("utf-8"), "123")

    def test_valid_converter_to_posint(self):
        response = self.client.get("/catalog/converter/123/")
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.content.decode("utf-8"), "123")
