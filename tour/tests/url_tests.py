from django.test import TestCase
from tour.urls import urlpatterns


class UrlsTest(TestCase):
    def test_that_urls_are_defined(self):
        """
        Should have several urls defined.
        """
        self.assertEqual(len(urlpatterns), 1)
