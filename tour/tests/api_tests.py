from django.contrib.auth.models import User
from django.test import TestCase
from django_dynamic_fixture import G
from mock import Mock
from tour.models import Tour
from tour.api import TourApiView


class TourApiViewTest(TestCase):

    def test_get_queryset(self):
        """
        Should return a queryset for tours
        """
        view = TourApiView()
        view.request = Mock(user=G(User, id=1))
        self.assertEqual(Tour, view.get_queryset().model)
