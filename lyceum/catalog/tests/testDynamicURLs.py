from http import HTTPStatus

from django.test import Client, TestCase
from parameterized import parameterized

from lyceum.middleware import ReverseRussianWordsMiddleware


class TestDynamicURL(TestCase):
    def setUp(self):
        super().setUp()
        ReverseRussianWordsMiddleware.response_count = 0

    def tearDown(self):
        super().tearDown()

    @parameterized.expand(
        [
            ("positive_number", 1, HTTPStatus.OK),
            ("negative_number", -1, HTTPStatus.NOT_FOUND),
            ("zero_number", 0, HTTPStatus.NOT_FOUND),
            ("not_number", "dd", HTTPStatus.NOT_FOUND),
            ("empty", "", HTTPStatus.NOT_FOUND),
        ],
    )
    def test_catalog_with_index_endpoint_status(
        self,
        test_name,
        index,
        status,
    ):
        client = Client()

        response = client.get(f"/catalog/{index}/")
        self.assertEqual(response.status_code, status)

    @parameterized.expand(
        [
            ("positive_number", 1, HTTPStatus.OK),
            ("negative_number", -1, HTTPStatus.NOT_FOUND),
            ("zero_number", 0, HTTPStatus.NOT_FOUND),
            ("not_number", "dd", HTTPStatus.NOT_FOUND),
            ("empty", "", HTTPStatus.NOT_FOUND),
        ],
    )
    def test_catalog_with_positive_number_regex_status(
        self,
        test_name,
        index,
        status,
    ):
        client = Client()

        response = client.get(f"/catalog/re/{index}/")
        self.assertEqual(response.status_code, status)

    @parameterized.expand(
        [
            ("positive_number", 1, HTTPStatus.OK),
            ("negative_number", -1, HTTPStatus.NOT_FOUND),
            ("zero_number", 0, HTTPStatus.NOT_FOUND),
            ("not_number", "dd", HTTPStatus.NOT_FOUND),
            ("empty", "", HTTPStatus.NOT_FOUND),
        ],
    )
    def test_catalog_with_converter_to_posint_status(
        self,
        test_name,
        index,
        status,
    ):
        client = Client()

        response = client.get(f"/catalog/converter/{index}/")
        self.assertEqual(response.status_code, status)


__all__ = ["TestDynamicURL"]
