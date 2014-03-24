from django.contrib.auth.models import User
from django.test import TestCase

from tour.models import Tour, Step, TourStatus
from tour.tests.mocks import MockTour, MockStep1, MockStep2, MockTour2, MockStep3, MockStep4


class TourTest(TestCase):

    def setUp(self):
        super(TourTest, self).setUp()
        self.reset_mock_tour_states()
        self.test_user = User.objects.create_user('test', 'test@gmail.com', 'test')
        self.test_user2 = User.objects.create_user('test2', 'test2@gmail.com', 'test2')

    def login_user1(self):
        self.client.login(username='test', password='test')

    def login_user2(self):
        self.client.login(username='test2', password='test2')

    def reset_mock_tour_states(self):
        mock_steps = [MockStep1, MockStep2, MockStep3, MockStep4]
        for mock_step in mock_steps:
            mock_step.complete = False

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

    def test_user_functions(self):
        """
        Verifies that a user can be assigned a tour only once
        Tests fetching an active tour for a user
        """
        self.assertIsNone(Tour.objects.get_for_user(self.test_user))

        # Create a single tour
        MockTour.create()

        # Add a user
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
