from django.contrib.auth.models import User
from django.test import TestCase
from tour.exceptions import MissingStepClass, MissingTourClass

from tour.models import Tour, Step, TourStatus
from tour.tests.mocks import MockTour, MockStep1, MockStep2, MockTour2, MockStep3, MockStep4, MockTour3, MockTour4, CompleteTour
from tour.tours import BaseStep


class TourTest(TestCase):

    def setUp(self):
        super(TourTest, self).setUp()
        self.reset_mock_tour_states()
        self.test_user = User.objects.create_user('test', 'test@gmail.com', 'test')
        self.test_user2 = User.objects.create_user('test2', 'test2@gmail.com', 'test2')

    def reset_mock_tour_states(self):
        mock_steps = [MockStep1, MockStep2, MockStep3, MockStep4]
        for mock_step in mock_steps:
            mock_step.complete = False

    def test_empty_url(self):
        """
        Verifies that the base step does not return a url
        """
        self.assertIsNone(BaseStep.get_url())

    def test_is_complete(self):
        """
        Verifies that the base step is never complete
        """
        self.assertFalse(BaseStep(None).is_complete(self.test_user))

    def test_exceptions(self):
        """
        Verifies that an exception is raised when there is no step class or tour class
        """
        with self.assertRaises(MissingStepClass):
            MockTour3.create()

        with self.assertRaises(MissingTourClass):
            MockTour4.create()

    def test_create(self):
        """
        Verifies that the tour gets created only once
        """
        # Create a single tour
        MockTour.create()
        self.assertEqual(1, Tour.objects.all().count())
        self.assertEqual(len(MockTour.steps), Step.objects.all().count())

        # Try to create a duplicate
        MockTour.create()
        self.assertEqual(1, Tour.objects.all().count())
        self.assertEqual(len(MockTour.steps), Step.objects.all().count())

    def test_delete(self):
        """
        Verifies that a tour and its steps get deleted
        """
        MockTour.create()
        MockTour2.create()
        self.assertTrue(2, Tour.objects.count())
        self.assertTrue(4, Step.objects.count())

        MockTour.delete()
        self.assertTrue(1, Tour.objects.count())
        self.assertTrue(2, Step.objects.count())

    def test_mark_complete(self):
        """
        Verifies that tours get marked as complete per user or for all users
        """
        MockTour.add_user(self.test_user)
        MockTour.add_user(self.test_user2)
        self.assertEqual(2, TourStatus.objects.filter(complete=False).count())
        tour_class = Tour.objects.get_for_user(self.test_user)
        tour_class.mark_complete(user=self.test_user)
        self.assertEqual(1, TourStatus.objects.filter(complete=False).count())
        MockTour.add_user(self.test_user)
        self.assertEqual(2, TourStatus.objects.filter(complete=False).count())
        tour_class = Tour.objects.get().load_tour_class()
        tour_class.mark_complete()
        self.assertEqual(0, TourStatus.objects.filter(complete=False).count())

    def test_user_functions(self):
        """
        Makes sure a tour is created when adding a user to a tour that doesn't exist
        Verifies that a user can be assigned a tour only once
        Tests fetching an active tour for a user
        """
        self.assertIsNone(Tour.objects.get_for_user(self.test_user))

        # Create a single tour
        MockTour.create()

        # Add a user
        MockTour.add_user(self.test_user)
        self.assertEqual(1, TourStatus.objects.all().count())

        # Delete all tours and make sure a tour is created when adding a user
        Tour.objects.all().delete()
        self.assertEqual(0, TourStatus.objects.all().count())
        MockTour.add_user(self.test_user)
        self.assertEqual(1, TourStatus.objects.all().count())

        # Try to add the user again
        MockTour.add_user(self.test_user)
        self.assertEqual(1, TourStatus.objects.all().count())

        # Fetch the tour
        tour_class = Tour.objects.get_for_user(self.test_user)
        self.assertIsNotNone(tour_class)

        # Set the tours as complete
        MockStep1.complete = True
        MockStep2.complete = True

        # Check if MockTour is complete
        tour_class = Tour.objects.get_for_user(self.test_user)
        self.assertIsNone(tour_class)

        # Make sure a second tour will be added
        MockTour.add_user(self.test_user)
        self.assertEqual(2, TourStatus.objects.all().count())
        self.assertEqual(1, TourStatus.objects.filter(complete=False).count())

    def test_nested_tour(self):
        """
        Verifies that records get created properly for nested tours
        """
        MockTour.create()
        MockTour2.create()
        self.assertEqual(4, Step.objects.all().count())
        steps = list(Step.objects.all().order_by('id'))
        self.assertEqual(steps[0].parent_step, None)
        self.assertEqual(steps[1].parent_step, None)
        self.assertEqual(steps[2].parent_step, steps[0])
        self.assertEqual(steps[3].parent_step, steps[0])

    def test_url(self):
        """
        Verifies that the tour returns the correct next url
        """
        # Create the tours
        MockTour.create()
        MockTour2.create()

        # Add a user
        MockTour.add_user(self.test_user)

        # Fetch the tour
        tour_class = Tour.objects.get_for_user(self.test_user)

        # Get the url
        url = tour_class.get_next_url()
        self.assertEqual('mock1', url)

        MockStep1.complete = True
        tour_class = Tour.objects.get_for_user(self.test_user)
        url = tour_class.get_next_url()
        self.assertEqual('mock3', url)

        MockStep3.complete = True
        tour_class = Tour.objects.get_for_user(self.test_user)
        url = tour_class.get_next_url()
        self.assertEqual('mock4', url)

        MockStep4.complete = True
        tour_class = Tour.objects.get_for_user(self.test_user)
        url = tour_class.get_next_url()
        self.assertEqual('mock2', url)

        MockStep2.complete = True
        tour_class = Tour.objects.get_for_user(self.test_user)
        self.assertIsNone(tour_class)

        # Check that no url is returned for a complete tour
        Tour.objects.all().delete()
        Step.objects.all().delete()
        CompleteTour.add_user(self.test_user)
        tour_class = Tour.objects.get().load_tour_class()
        url = tour_class.get_next_url()
        self.assertIsNone(url)

    def test_url_list(self):
        """
        Verifies that the tour builds the url list correctly
        """
        # Create the tours
        MockTour.create()
        MockTour2.create()

        # Add a user
        MockTour.add_user(self.test_user)

        # Fetch the tour
        tour_class = Tour.objects.get_for_user(self.test_user)

        urls = tour_class.get_url_list()
        expected_urls = ['mock1', 'mock3', 'mock4', 'mock2']
        self.assertEqual(expected_urls, urls)
