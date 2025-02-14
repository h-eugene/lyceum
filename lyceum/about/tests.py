from http import HTTPStatus

import django.test

from lyceum.middleware import ReverseRussianWordsMiddleware


class TestStaticURL(django.test.TestCase):
    def setUp(self):
        ReverseRussianWordsMiddleware.response_count = 0

    def test_about_endpoint_status(self):
        client = django.test.Client()

        response = client.get("/about/")

        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_about_endpoint_content(self):
        client = django.test.Client()

        response = client.get("/about/")
        word = "О проекте"

        self.assertEqual(
            response.content.decode("utf-8"),
            "<body>" + word + "</body>",
        )
