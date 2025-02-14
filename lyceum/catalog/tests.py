from http import HTTPStatus

from django.test import Client, TestCase

from lyceum.middleware import ReverseRussianWordsMiddleware

from parameterized import parameterized


class TestStaticURL(TestCase):
    def setUp(self):
        ReverseRussianWordsMiddleware.response_count = 0

    def test_default_catalog_endpoint_status(self):
        client = Client()

        response = client.get("/catalog/")

        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_default_catalog_endpoint_content(self):
        client = Client()

        response = client.get("/catalog/")
        text = "Список элементов"

        self.assertEqual(
            response.content.decode("utf-8"),
            "<body>" + text + "</body>",
        )


class TestDynamicURL(TestCase):
    def setUp(self):
        ReverseRussianWordsMiddleware.response_count = 0

    @parameterized.expand(
        [
            ("positive_number", 1, HTTPStatus.OK),
            ("negative_number", -1, HTTPStatus.NOT_FOUND),
            ("zero_number", 0, HTTPStatus.OK),
            ("not_number", "dd", HTTPStatus.NOT_FOUND),
            ("empty", "", HTTPStatus.NOT_FOUND),
        ]
    )
    def test_catalog_with_index_endpoint_status(
        self, test_name, index, status
    ):
        client = Client()

        response = client.get(f"/catalog/{index}/")
        self.assertEqual(response.status_code, status)

    def test_catalog_with_index_endpoint_content(self):
        client = Client()

        response = client.get("/catalog/1/")
        text = "Подробно элемент"

        self.assertEqual(
            response.content.decode("utf-8"),
            "<body>" + text + "</body>",
        )

    @parameterized.expand(
        [
            ("positive_number", 1, HTTPStatus.OK),
            ("negative_number", -1, HTTPStatus.NOT_FOUND),
            ("zero_number", 0, HTTPStatus.NOT_FOUND),
            ("not_number", "dd", HTTPStatus.NOT_FOUND),
            ("empty", "", HTTPStatus.NOT_FOUND),
        ]
    )
    def test_catalog_with_not_negative_number_regex_status(
        self, test_name, index, status
    ):
        client = Client()

        response = client.get(f"/catalog/re/{index}/")
        self.assertEqual(response.status_code, status)

    def test_catalog_with_positive_number_regex_content(self):
        client = Client()

        response = client.get("/catalog/re/123/")
        self.assertEqual(response.content.decode("utf-8"), "123")

    @parameterized.expand(
        [
            ("positive_number", 1, HTTPStatus.OK),
            ("negative_number", -1, HTTPStatus.NOT_FOUND),
            ("zero_number", 0, HTTPStatus.NOT_FOUND),
            ("not_number", "dd", HTTPStatus.NOT_FOUND),
            ("empty", "", HTTPStatus.NOT_FOUND),
        ]
    )
    def test_catalog_with_converter_to_posint_status(
        self, test_name, index, status
    ):
        client = Client()

        response = client.get(f"/catalog/converter/{index}/")
        self.assertEqual(response.status_code, status)

    def test_catalog_with_converter_to_posint_content(self):
        client = Client()

        response = client.get("/catalog/converter/123/")
        self.assertEqual(response.content.decode("utf-8"), "123")
