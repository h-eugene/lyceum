from http import HTTPStatus

import django.test


class TestStaticURL(django.test.TestCase):
    def test_about_endpoint(self):
        # О проекте
        client = django.test.Client()
        for i in range(1, 21):
            response = client.get("/about/")
            word = "О проекте"
            if i % 10 == 0:
                # Переворачиваем каждое слово
                word = ' '.join(map(lambda x: x[::-1], word.split()))

            self.assertEqual(response.status_code, HTTPStatus.OK)
            self.assertEqual(
                response.content.decode("utf-8"),
                "<body>" + word + "</body>",
            )
