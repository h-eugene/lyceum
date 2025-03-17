from http import HTTPStatus

from django.test import Client, TestCase
from django.urls import reverse
from parameterized import parameterized

from lyceum.middleware import ReverseRussianWordsMiddleware


class TestDynamicURL(TestCase):
    def setUp(self):
        super().setUp()
        ReverseRussianWordsMiddleware.response_count = 0

    def tearDown(self):
        super().tearDown()

    testCases = [
        ("positive_number", 1, HTTPStatus.OK),
        ("negative_number", -1, HTTPStatus.NOT_FOUND),
        ("zero_number", 0, HTTPStatus.NOT_FOUND),
        ("not_number", "dd", HTTPStatus.NOT_FOUND),
        ("empty", "", HTTPStatus.NOT_FOUND),
    ]

    @parameterized.expand(testCases)
    def test_catalog_with_index_endpoint_status(
        self,
        test_name,
        index,
        status,
    ):
        client = Client()
        url = reverse("catalog:item_list") + f"{index}/"
        response = client.get(url)
        self.assertEqual(response.status_code, status)

    @parameterized.expand(testCases)
    def test_catalog_with_positive_number_regex_status(
        self,
        test_name,
        index,
        status,
    ):
        client = Client()
        url = reverse("catalog:item_list") + f"re/{index}/"
        response = client.get(url)
        self.assertEqual(response.status_code, status)

    @parameterized.expand(testCases)
    def test_catalog_with_converter_to_posint_status(
        self,
        test_name,
        index,
        status,
    ):
        client = Client()
        url = reverse("catalog:item_list") + f"converter/{index}/"
        response = client.get(url)
        self.assertEqual(response.status_code, status)


__all__ = ["TestDynamicURL"]
