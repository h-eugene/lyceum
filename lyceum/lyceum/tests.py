import django.test


class TestStaticURL(django.test.TestCase):
    def test_homepage_endpoint(self):
        response = django.test.Client().get("/")
        self.assertEqual(response.status_code, 200)

    def test_about_endpoint(self):
        response = django.test.Client().get("/about/")
        self.assertEqual(response.status_code, 200)

    def test_default_catalog_endpoint(self):
        response = django.test.Client().get("/catalog/")
        self.assertEqual(response.status_code, 200)

    def test_catalog_with_index_endpoint(self):
        response = django.test.Client().get("/catalog/1/")
        self.assertEqual(response.status_code, 200)
