from django.contrib.auth.models import User
from django.test import TestCase
from django_dynamic_fixture import G
from mock import patch
from tour.models import Tour, TourStatus, Step
from tour.tests.tour_tests import BaseTourTest


class TourManagerTest(BaseTourTest):
    """
    Tests the methods of the TourManager
    """
    @patch('tour.tests.mocks.MockStep1.is_complete', spec_set=True)
    def test_complete_tours(self, mock_step1_is_complete):
        """
        Verifies that any completed tours get marked as complete
        :type mock_step1_is_complete: Mock
        """
        mock_step1_is_complete.return_value = False
        self.tour1.steps.add(self.step1)

        # add user to tours
        self.tour1.load_tour_class().add_user(self.test_user)
        self.tour2.load_tour_class().add_user(self.test_user)

        Tour.objects.complete_tours(self.test_user)
        self.assertEqual(1, TourStatus.objects.filter(complete=True).count())
        self.assertEqual(1, TourStatus.objects.filter(complete=False).count())

    def test_complete_tours_no_user(self):
        """
        Makes sure None is returned if the user is anonymous
        """
        self.assertIsNone(Tour.objects.complete_tours(User()))

    @patch('tour.tests.mocks.MockStep1.is_complete', spec_set=True)
    def test_get_for_user(self, mock_step1_is_complete):
        """
        Verifies that an incomplete tour class is fetched for a user
        :type mock_step1_is_complete: Mock
        """
        mock_step1_is_complete.return_value = False
        self.tour1.steps.add(self.step1)
        self.tour2.steps.add(self.step2)

        # add users to tours
        self.tour1.load_tour_class().add_user(self.test_user)
        self.tour1.load_tour_class().add_user(self.test_user2)
        self.tour2.load_tour_class().add_user(self.test_user)
        self.tour2.load_tour_class().add_user(self.test_user2)

        # tour 2 will be completed, so check for tour 1
        self.assertEqual(self.tour1, Tour.objects.get_for_user(self.test_user))

    def test_get_for_user_no_user(self):
        """
        Makes sure None is returned if the user is anonymous
        """
        self.assertIsNone(Tour.objects.get_for_user(User()))

    def test_get_for_user_empty(self):
        """
        Verifies that None is returned if no incomplete tours
        """
        self.tour1.steps.add(self.step1)

        # add user to tour
        self.tour1.load_tour_class().add_user(self.test_user)
        self.tour1.load_tour_class().add_user(self.test_user2)
        self.tour2.load_tour_class().add_user(self.test_user)
        self.tour2.load_tour_class().add_user(self.test_user2)

        # all tours should be completed
        self.assertIsNone(Tour.objects.get_for_user(self.test_user))

    def test_get_recent_tour_complete(self):
        """
        Makes sure that a recently completed tour is returned. Verifies most recently completed tour
        is returned
        """
        # add user to tour
        self.tour1.load_tour_class().add_user(self.test_user)
        self.tour1.load_tour_class().add_user(self.test_user2)
        self.tour2.load_tour_class().add_user(self.test_user)
        self.tour2.load_tour_class().add_user(self.test_user2)

        # complete tours
        self.tour2.load_tour_class().mark_complete(self.test_user)
        self.tour1.load_tour_class().mark_complete(self.test_user)
        self.tour1.load_tour_class().mark_complete(self.test_user2)

        # make sure complete
        self.assertEqual(3, TourStatus.objects.filter(complete=True).count())

        # check that correct tour is returned
        self.assertEqual(self.tour1, Tour.objects.get_recent_tour(self.test_user))

    def test_get_recent_tour_no_user(self):
        """
        Makes sure None is returned if the user is anonymous
        """
        self.assertIsNone(Tour.objects.get_recent_tour(User()))

    def test_get_recent_tour_incomplete(self):
        """
        Makes sure that an incomplete tour is returned before a complete tour
        """
        # add user to tour
        self.tour1.load_tour_class().add_user(self.test_user)
        self.tour1.load_tour_class().add_user(self.test_user2)
        self.tour2.load_tour_class().add_user(self.test_user)
        self.tour2.load_tour_class().add_user(self.test_user2)

        # complete tours
        self.tour1.load_tour_class().mark_complete(self.test_user)
        self.tour2.load_tour_class().mark_complete(self.test_user)
        self.tour1.load_tour_class().mark_complete(self.test_user2)

        # make sure complete
        self.assertEqual(3, TourStatus.objects.filter(complete=True).count())

        # check that correct tour is returned
        self.assertEqual(self.tour2, Tour.objects.get_recent_tour(self.test_user2))

    def test_get_recent_tour_none(self):
        """
        Makes sure None is returned if there is no completed tour
        """
        self.assertIsNone(Tour.objects.get_recent_tour(self.test_user))

    @patch('tour.tests.mocks.MockStep1.is_complete', spec_set=True)
    @patch('tour.models.TourManager.get_for_user')
    def test_get_next_url_current_tour(self, mock_get_for_user, mock_step1_is_complete):
        """
        Verifies that the next url of a tour will be returned
        :type mock_get_for_user: Mock
        :type mock_step1_is_complete: Mock
        """
        mock_get_for_user.return_value = self.tour1
        mock_step1_is_complete.return_value = False

        self.tour1.steps.add(self.step1)

        # add user to tour
        self.tour1.load_tour_class().add_user(self.test_user)
        self.tour1.load_tour_class().add_user(self.test_user2)
        self.tour2.load_tour_class().add_user(self.test_user)
        self.tour2.load_tour_class().add_user(self.test_user2)

        self.assertEqual(self.step1.url, Tour.objects.get_next_url(self.test_user))
        self.assertEqual(1, mock_get_for_user.call_count)

    @patch('tour.tests.mocks.MockStep1.is_complete', spec_set=True)
    @patch('tour.models.TourManager.get_recent_tour')
    @patch('tour.models.TourManager.get_for_user')
    def test_get_next_url_recent_tour(self, mock_get_for_user, mock_get_recent_tour, mock_step1_is_complete):
        """
        Verifies that the next url of a recent tour will be returned
        :type mock_get_for_user: Mock
        :type mock_get_recent_tour: Mock
        :type mock_step1_is_complete: Mock
        """
        mock_get_for_user.return_value = None
        mock_get_recent_tour.return_value = self.tour2
        mock_step1_is_complete.return_value = False

        self.tour2.steps.add(self.step1)

        # add user to tour
        self.tour1.load_tour_class().add_user(self.test_user)
        self.tour1.load_tour_class().add_user(self.test_user2)
        self.tour2.load_tour_class().add_user(self.test_user)
        self.tour2.load_tour_class().add_user(self.test_user2)

        self.assertEqual(self.step1.url, Tour.objects.get_next_url(self.test_user))
        self.assertEqual(1, mock_get_for_user.call_count)
        self.assertEqual(1, mock_get_recent_tour.call_count)

    def test_get_next_url_no_user(self):
        """
        Makes sure None is returned if the user is anonymous
        """
        self.assertIsNone(Tour.objects.get_next_url(User()))

    def test_get_next_url_none(self):
        """
        Verifies that None is returned if no tours exist for a user
        """
        self.assertIsNone(Tour.objects.get_next_url(self.test_user))


class TourTest(TestCase):

    def test_str(self):
        """
        Tests the tour str method
        """
        tour = G(Tour, display_name='test1')
        self.assertEqual('test1', str(tour))


class StepTest(TestCase):

    def test_str(self):
        """
        Tests the step str method
        """
        step = G(Step, display_name='test1')
        self.assertEqual('test1', str(step))
