from http import HTTPStatus

from django.test import Client, TestCase

from lyceum.middleware import ReverseRussianWordsMiddleware


class TestStaticURL(TestCase):
    def setUp(self):
        super().setUp()
        ReverseRussianWordsMiddleware.response_count = 0

    def tearDown(self):
        super().tearDown()

    def test_about_endpoint_status(self):
        client = Client()

        response = client.get("/about/")

        self.assertEqual(response.status_code, HTTPStatus.OK)
