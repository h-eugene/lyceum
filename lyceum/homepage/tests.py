from http import HTTPStatus

import django.test


class TestStaticURL(django.test.TestCase):
    def test_homepage_endpoint(self):
        response = django.test.Client().get("/")
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_homepage_coffee_endpoint(self):
        response = django.test.Client().get("/coffee/")
        self.assertEqual(response.status_code, HTTPStatus.IM_A_TEAPOT)
        self.assertEqual(
            response.content.decode("utf-8"), "Я чайник"
        )
