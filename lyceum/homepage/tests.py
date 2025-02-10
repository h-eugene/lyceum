from http import HTTPStatus
import django.test

from lyceum.middleware import ReverseRussianWordsMiddleware


class TestStaticURL(django.test.TestCase):
    def setUp(self):
        ReverseRussianWordsMiddleware.response_count = 0

    def test_homepage_endpoint(self):
        client = django.test.Client()

        for i in range(1, 21):
            response = client.get("/")
            word = "Главная"
            if i % 10 == 0:
                word = word[::-1]

            self.assertEqual(response.status_code, HTTPStatus.OK)
            self.assertEqual(
                response.content.decode("utf-8"), "<body>" + word + "</body>"
            )

    def test_homepage_coffee_endpoint(self):
        client = django.test.Client()

        for i in range(1, 21):
            response = client.get("/coffee/")
            word = "Я чайник"
            if i % 10 == 0:
                # Переворачиваем каждое слово
                word = " ".join(map(lambda x: x[::-1], word.split()))

            self.assertEqual(response.status_code, HTTPStatus.IM_A_TEAPOT)
            self.assertEqual(
                response.content.decode("utf-8"), "<body>" + word + "</body>"
            )
