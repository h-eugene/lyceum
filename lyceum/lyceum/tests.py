from django.conf import settings
from django.test import Client, override_settings, TestCase

from lyceum.middleware import ReverseRussianWordsMiddleware


class TestMiddlwareWithAllowReverse(TestCase):
    def setUp(self):
        super().setUp()
        ReverseRussianWordsMiddleware.response_count = 0

    def test_homepage_endpoint_content(
        self,
    ):
        client = Client()
        with override_settings(ALLOW_REVERSE=True):
            for i in range(1, 21):
                response = client.get("/")
                text = "Главная"
                if i % 10 == 0 and settings.ALLOW_REVERSE:
                    text = text[::-1]

                self.assertEqual(
                    response.content.decode("utf-8"),
                    "<body>" + text + "</body>",
                )

    def test_homepage_coffee_endpoint_content(self):
        client = Client()

        with override_settings(ALLOW_REVERSE=True):
            for i in range(1, 21):
                response = client.get("/coffee/")
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
                response = client.get("/coffee/")
                response2 = client2.get("/coffee/")
                text = "Я чайник"
                text2 = text
                if i % 5 == 0 and settings.ALLOW_REVERSE:
                    text2 = " ".join(i[::-1] for i in text.split())
                self.assertEqual(response.content.decode(), text)
                self.assertEqual(response2.content.decode(), text2)

    def test_about_endpoint_content(self):
        client = Client()

        with override_settings(ALLOW_REVERSE=True):
            for i in range(1, 21):
                response = client.get("/about/")
                text = "О проекте"

                if i % 10 == 0 and settings.ALLOW_REVERSE:
                    text = " ".join(i[::-1] for i in text.split())

                self.assertEqual(
                    response.content.decode("utf-8"),
                    "<body>" + text + "</body>",
                )

    def test_default_catalog_endpoint_content(self):
        client = Client()

        with override_settings(ALLOW_REVERSE=True):
            for i in range(1, 21):
                response = client.get("/catalog/")
                text = "Список элементов"

                if i % 10 == 0 and settings.ALLOW_REVERSE:
                    text = " ".join(i[::-1] for i in text.split())

                self.assertEqual(
                    response.content.decode("utf-8"),
                    "<body>" + text + "</body>",
                )

    def test_catalog_with_index_endpoint_content(self):
        client = Client()

        with override_settings(ALLOW_REVERSE=True):
            for i in range(1, 21):
                response = client.get("/catalog/1/")
                text = "Подробно элемент"

                if i % 10 == 0 and settings.ALLOW_REVERSE:
                    text = " ".join(i[::-1] for i in text.split())

                self.assertEqual(
                    response.content.decode("utf-8"),
                    "<body>" + text + "</body>",
                )


class TestMiddlwareWithoutAllowReverse(TestCase):
    def setUp(self):
        ReverseRussianWordsMiddleware.response_count = 0

    def test_homepage_endpoint_content(
        self,
    ):
        client = Client()
        with override_settings(ALLOW_REVERSE=False):
            for i in range(1, 21):
                response = client.get("/")
                text = "Главная"
                if i % 10 == 0 and settings.ALLOW_REVERSE:
                    text = text[::-1]

                self.assertEqual(
                    response.content.decode("utf-8"),
                    "<body>" + text + "</body>",
                )

    def test_homepage_coffee_endpoint_content(self):
        client = Client()

        with override_settings(ALLOW_REVERSE=False):
            for i in range(1, 21):
                response = client.get("/coffee/")
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
                response = client.get("/coffee/")
                response2 = client2.get("/coffee/")
                text = "Я чайник"
                text2 = text
                if i % 5 == 0 and settings.ALLOW_REVERSE:
                    text2 = " ".join(i[::-1] for i in text.split())
                self.assertEqual(response.content.decode(), text)
                self.assertEqual(response2.content.decode(), text2)

    def test_about_endpoint_content(self):
        client = Client()

        with override_settings(ALLOW_REVERSE=False):
            for i in range(1, 21):
                response = client.get("/about/")
                text = "О проекте"

                if i % 10 == 0 and settings.ALLOW_REVERSE:
                    text = " ".join(i[::-1] for i in text.split())

                self.assertEqual(
                    response.content.decode("utf-8"),
                    "<body>" + text + "</body>",
                )

    def test_default_catalog_endpoint_content(self):
        client = Client()

        with override_settings(ALLOW_REVERSE=False):
            for i in range(1, 21):
                response = client.get("/catalog/")
                text = "Список элементов"

                if i % 10 == 0 and settings.ALLOW_REVERSE:
                    text = " ".join(i[::-1] for i in text.split())

                self.assertEqual(
                    response.content.decode("utf-8"),
                    "<body>" + text + "</body>",
                )

    def test_catalog_with_index_endpoint_content(self):
        client = Client()

        with override_settings(ALLOW_REVERSE=False):
            for i in range(1, 21):
                response = client.get("/catalog/1/")
                text = "Подробно элемент"

                if i % 10 == 0 and settings.ALLOW_REVERSE:
                    text = " ".join(i[::-1] for i in text.split())

                self.assertEqual(
                    response.content.decode("utf-8"),
                    "<body>" + text + "</body>",
                )
