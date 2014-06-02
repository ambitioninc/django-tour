from django.test import TestCase
from django_dynamic_fixture import G
from tour.tests.mocks import MockTour, MockStep1
from tour.models import Tour, Step


class TourTest(TestCase):
    """
    Tests the methods of the Tour class
    """
    def test_load_tour_class(self):
        tour = G(
            Tour, display_name='Mock Tour', name='tour1', complete_url='mock_complete1',
            tour_class='tour.tests.mocks.MockTour')
        self.assertEqual(tour.load_tour_class().__class__, MockTour)


class StepTest(TestCase):
    """
    Tests the methods of the Step class
    """
    def test_load_step_class(self):
        step = G(
            Step, step_class='tour.tests.mocks.MockStep1', display_name='Mock Step 1', name='mock1', url='mock1')
        self.assertEqual(step.load_step_class().__class__, MockStep1)
