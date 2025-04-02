from django.conf import settings
from django.test import Client, TestCase, override_settings
from django.urls import reverse

from lyceum.middleware import ReverseRussianWordsMiddleware


class TestMiddlwareWithAllowReverse(TestCase):
    def setUp(self):
        super().setUp()
        ReverseRussianWordsMiddleware.response_count = 0

    def tearDown(self):
        super().tearDown()

    def test_homepage_coffee_endpoint_content(self):
        client = Client()

        with override_settings(ALLOW_REVERSE=True):
            for i in range(1, 21):
                url = reverse("homepage:coffee")
                response = client.get(url)
                text = "Я чайник"
                if i % 10 == 0 and settings.ALLOW_REVERSE:
                    # Переворачиваем каждое слово
                    text = " ".join(i[::-1] for i in text.split())

                self.assertEqual(response.content.decode("utf-8"), text)

    def test_homepage_coffee_endpoint_content_with_two_clients(self):
        client2 = Client()
        client = Client()

        with override_settings(ALLOW_REVERSE=True):
            for i in range(1, 21):
                url = reverse("homepage:coffee")
                response = client.get(url)
                response2 = client2.get(url)
                text = "Я чайник"
                text2 = text
                if i % 5 == 0 and settings.ALLOW_REVERSE:
                    text2 = " ".join(i[::-1] for i in text.split())
                self.assertEqual(response.content.decode(), text)
                self.assertEqual(response2.content.decode(), text2)


class TestMiddlwareWithoutAllowReverse(TestCase):
    def setUp(self):
        ReverseRussianWordsMiddleware.response_count = 0

    def tearDown(self):
        super().tearDown()

    def test_homepage_coffee_endpoint_content(self):
        client = Client()

        with override_settings(ALLOW_REVERSE=False):
            for i in range(1, 21):
                url = reverse("homepage:coffee")
                response = client.get(url)
                text = "Я чайник"
                if i % 10 == 0 and settings.ALLOW_REVERSE:
                    # Переворачиваем каждое слово
                    text = " ".join(i[::-1] for i in text.split())

                self.assertEqual(response.content.decode("utf-8"), text)

    def test_homepage_coffee_endpoint_content_with_two_clients(self):
        client2 = Client()
        client = Client()

        with override_settings(ALLOW_REVERSE=False):
            for i in range(1, 21):
                url = reverse("homepage:coffee")
                response = client.get(url)
                response2 = client2.get(url)
                text = "Я чайник"
                text2 = text
                if i % 5 == 0 and settings.ALLOW_REVERSE:
                    text2 = " ".join(i[::-1] for i in text.split())
                self.assertEqual(response.content.decode(), text)
                self.assertEqual(response2.content.decode(), text2)


__all__ = []
