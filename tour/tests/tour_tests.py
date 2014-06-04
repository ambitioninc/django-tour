from django.contrib.auth.models import User
from django.test import TestCase
from django_dynamic_fixture import G

from tour.models import Tour, Step, TourStatus


class BaseTourTest(TestCase):
    """
    Provides basic setup for tour tests like creating users
    """
    def setUp(self):
        super(BaseTourTest, self).setUp()
        self.test_user = User.objects.create_user('test', 'test@gmail.com', 'test')
        self.test_user2 = User.objects.create_user('test2', 'test2@gmail.com', 'test2')

        self.tour1 = G(
            Tour, display_name='Mock Tour', name='tour1', complete_url='mock_complete1',
            tour_class='tour.tests.mocks.MockTour')
        self.tour2 = G(
            Tour, display_name='Mock Tour 2', name='tour2', complete_url='mock_complete2',
            tour_class='tour.tests.mocks.MockTour2')
        self.step1 = G(
            Step, step_class='tour.tests.mocks.MockStep1', display_name='Mock Step 1', name='mock1',
            url='mock1', parent_step=None, sort_order=0)
        self.step2 = G(
            Step, step_class='tour.tests.mocks.MockStep2', display_name='Mock Step 2', name='mock2',
            url='mock2', parent_step=None, sort_order=1)
        self.step3 = G(
            Step, step_class='tour.tests.mocks.MockStep3', display_name='Mock Step 3', name='mock3',
            url='mock3', parent_step=None, sort_order=2)
        self.step4 = G(
            Step, step_class='tour.tests.mocks.MockStep4', display_name='Mock Step 4', name='mock4',
            url='mock4', parent_step=None, sort_order=3)

    def login_user1(self):
        self.client.login(username='test', password='test')

    def login_user2(self):
        self.client.login(username='test2', password='test2')


class TourTest(BaseTourTest):
    """
    Tests the functionality of the Tour and Step classes
    """
    def test_init(self):
        """
        Verifies that the tour object is properly set when loaded
        """
        self.assertEqual(self.tour1.load_tour_class().tour, self.tour1)

    def test_get_steps_flat(self):
        """
        Verifies that the steps are loaded in the correct order
        """
        self.step1.sort_order = 1
        self.step1.save()
        self.step2.sort_order = 0
        self.step2.save()

        self.tour1.steps.add(self.step1, self.step2)
        expected_steps = [self.step2, self.step1]
        self.assertEqual(expected_steps, self.tour1.load_tour_class().get_steps())

    def test_get_steps_nested(self):
        """
        Verifies that the nested steps are loaded correctly
        """
        self.tour1.steps.add(self.step1, self.step2)
        self.step1.steps.add(self.step3, self.step4)

        self.step3.sort_order = 1
        self.step3.save()
        self.step4.sort_order = 0
        self.step4.save()

        expected_steps = [self.step1, self.step4, self.step3, self.step2]
        self.assertEqual(expected_steps, self.tour1.load_tour_class().get_steps())

    def test_get_url_list(self):
        """
        Verifies that the tour returns the correct step url list
        """
        self.tour1.steps.add(self.step1, self.step2)
        expected_url_list = ['mock1', 'mock2']
        self.assertEqual(expected_url_list, self.tour1.load_tour_class().get_url_list())

    def test_add_user(self):
        """
        Verifies that a user is linked to a tour properly and that the correct tour is returned
        """
        # add user to tour
        tour_status = self.tour1.load_tour_class().add_user(self.test_user)

        # try to add again and make sure it returns the same status
        self.assertEqual(tour_status, self.tour1.load_tour_class().add_user(self.test_user))

        # make sure only one status
        self.assertEqual(1, TourStatus.objects.count())

        # mark status as complete
        tour_status.complete = True
        tour_status.save()

        # make sure another tour is created
        self.tour1.load_tour_class().add_user(self.test_user)
        self.assertEqual(2, TourStatus.objects.count())
        self.assertEqual(1, TourStatus.objects.filter(complete=False).count())

    def test_mark_complete(self):
        """
        Verifies that a tour status record will be marked as complete for a user
        """
        # add multiple users to multiple tours
        tour1_class = self.tour1.load_tour_class()
        tour2_class = self.tour2.load_tour_class()
        tour1_class.add_user(self.test_user)
        tour1_class.add_user(self.test_user2)
        tour2_class.add_user(self.test_user)
        tour2_class.add_user(self.test_user2)

        # make sure there are 4 records
        self.assertEqual(4, TourStatus.objects.count())
        # complete the tour for user1
        self.assertTrue(tour1_class.mark_complete(self.test_user))
        # make sure it is complete
        self.assertEqual(1, TourStatus.objects.filter(complete=True).count())
        # try to complete the same tour
        self.assertFalse(tour1_class.mark_complete(self.test_user))
        # add the user to the tour again
        tour1_class.add_user(self.test_user)
        # make sure there are 5 records
        self.assertEqual(5, TourStatus.objects.count())

    # def test_empty_url(self):
    #     """
    #     Verifies that the base step does not return a url
    #     """
    #     self.assertIsNone(BaseStep.get_url())
    #
    # def test_is_complete(self):
    #     """
    #     Verifies that the base step is never complete
    #     """
    #     step = Step(name=BaseStep.name, url=BaseStep.get_url())
    #     self.assertFalse(BaseStep(step).is_complete(self.test_user))
    #
    # def test_exceptions(self):
    #     """
    #     Verifies that an exception is raised when there is no step class or tour class
    #     """
    #     with self.assertRaises(MissingStepClass):
    #         MockTour3.create()
    #
    #     with self.assertRaises(MissingTourClass):
    #         MockTour4.create()
    #
    # def test_create(self):
    #     """
    #     Verifies that the tour gets created only once
    #     """
    #     # Create a single tour
    #     MockTour.create()
    #     self.assertEqual(1, Tour.objects.all().count())
    #     self.assertEqual(len(MockTour.steps), Step.objects.all().count())
    #
    #     # Try to create a duplicate
    #     MockTour.create()
    #     self.assertEqual(1, Tour.objects.all().count())
    #     self.assertEqual(len(MockTour.steps), Step.objects.all().count())
    #
    #     # Create a tour with a parent and make sure only the steps get added to the parent tour
    #     MockTour2.create()
    #     self.assertEqual(1, Tour.objects.count())
    #     self.assertEqual(4, Step.objects.count())
    #
    # def test_delete(self):
    #     """
    #     Verifies that a tour and its steps get deleted
    #     """
    #     MockTour.create()
    #     MockTour2.create()
    #     self.assertEqual(1, Tour.objects.count())
    #     self.assertEqual(4, Step.objects.count())
    #
    #     MockTour2.delete()
    #     self.assertEqual(1, Tour.objects.count())
    #     self.assertEqual(2, Step.objects.count())
    #
    #     MockTour.delete()
    #     self.assertEqual(0, Tour.objects.count())
    #     self.assertEqual(0, Step.objects.count())
    #
    # def test_mark_complete(self):
    #     """
    #     Verifies that tours get marked as complete per user or for all users
    #     """
    #     MockTour.add_user(self.test_user)
    #     MockTour.add_user(self.test_user2)
    #     self.assertEqual(2, TourStatus.objects.filter(complete=False).count())
    #     tour_class = Tour.objects.get_for_user(self.test_user)
    #     tour_class.mark_complete(user=self.test_user)
    #     self.assertEqual(1, TourStatus.objects.filter(complete=False).count())
    #     # make sure marking complete again returns false
    #     self.assertFalse(tour_class.mark_complete(user=self.test_user))
    #
    #     MockTour.add_user(self.test_user)
    #     self.assertEqual(2, TourStatus.objects.filter(complete=False).count())
    #     tour_class = Tour.objects.get().load_tour_class()
    #     tour_class.mark_complete()
    #     self.assertEqual(0, TourStatus.objects.filter(complete=False).count())
    #
    # def test_user_functions(self):
    #     """
    #     Makes sure a tour is created when adding a user to a tour that doesn't exist
    #     Verifies that a user can be assigned a tour only once
    #     Tests fetching an active tour for a user
    #     """
    #     self.assertIsNone(Tour.objects.get_for_user(User()))
    #     self.assertIsNone(Tour.objects.get_recent_tour(User()))
    #     self.assertIsNone(Tour.objects.get_for_user(self.test_user))
    #
    #     # Create a single tour
    #     MockTour.create()
    #
    #     # Add a user
    #     MockTour.add_user(self.test_user)
    #     self.assertEqual(1, TourStatus.objects.all().count())
    #
    #     # Delete all tours and make sure a tour is created when adding a user
    #     Tour.objects.all().delete()
    #     self.assertEqual(0, TourStatus.objects.all().count())
    #     MockTour.add_user(self.test_user)
    #     self.assertEqual(1, TourStatus.objects.all().count())
    #
    #     # Try to add the user again
    #     MockTour.add_user(self.test_user)
    #     self.assertEqual(1, TourStatus.objects.all().count())
    #
    #     # Fetch the tour
    #     tour_class = Tour.objects.get_for_user(self.test_user)
    #     self.assertIsNotNone(tour_class)
    #
    #     # Set the tours as complete
    #     MockStep1.complete = True
    #     MockStep2.complete = True
    #
    #     # Check if MockTour is complete
    #     tour_class = Tour.objects.get_for_user(self.test_user)
    #     self.assertIsNone(tour_class)
    #
    #     # Make sure we can get the most recent tour
    #     tour_class = Tour.objects.get_recent_tour(self.test_user)
    #     self.assertIsNotNone(tour_class)
    #
    #     # Make sure a second tour will be added
    #     MockTour.add_user(self.test_user)
    #     self.assertEqual(2, TourStatus.objects.all().count())
    #     self.assertEqual(1, TourStatus.objects.filter(complete=False).count())
    #
    # def test_nested_tour(self):
    #     """
    #     Verifies that records get created properly for nested tours
    #     """
    #     MockTour.create()
    #     MockTour2.create()
    #     self.assertEqual(4, Step.objects.all().count())
    #     steps = list(Step.objects.all().order_by('id'))
    #     self.assertEqual(steps[0].parent_step, None)
    #     self.assertEqual(steps[1].parent_step, None)
    #     self.assertEqual(steps[2].parent_step, steps[0])
    #     self.assertEqual(steps[3].parent_step, steps[0])
    #
    # def test_url(self):
    #     """
    #     Verifies that the tour returns the correct next url
    #     """
    #     # Create the tours
    #     MockTour.create()
    #     MockTour2.create()
    #
    #     # Add a user
    #     MockTour.add_user(self.test_user)
    #
    #     # Fetch the tour
    #     tour_class = Tour.objects.get_for_user(self.test_user)
    #
    #     # Get the url
    #     url = tour_class.get_next_url()
    #     self.assertEqual('mock1', url)
    #
    #     MockStep1.complete = True
    #     tour_class = Tour.objects.get_for_user(self.test_user)
    #     url = tour_class.get_next_url()
    #     self.assertEqual('mock3', url)
    #
    #     MockStep3.complete = True
    #     tour_class = Tour.objects.get_for_user(self.test_user)
    #     url = tour_class.get_next_url()
    #     self.assertEqual('mock4', url)
    #
    #     MockStep4.complete = True
    #     tour_class = Tour.objects.get_for_user(self.test_user)
    #     url = tour_class.get_next_url()
    #     self.assertEqual('mock2', url)
    #
    #     MockStep2.complete = True
    #     tour_class = Tour.objects.get_for_user(self.test_user)
    #     self.assertIsNone(tour_class)
    #
    #     # Check that no url is returned for a complete tour
    #     Tour.objects.all().delete()
    #     Step.objects.all().delete()
    #     CompleteTour.add_user(self.test_user)
    #     tour_class = Tour.objects.get().load_tour_class()
    #     self.assertTrue(tour_class.is_complete())
    #     url = tour_class.get_next_url()
    #     self.assertEqual('mock_complete', url)
    #
    # def test_url_list(self):
    #     """
    #     Verifies that the tour builds the url list correctly
    #     """
    #     # Create the tours
    #     MockTour.create()
    #     MockTour2.create()
    #
    #     # Add a user
    #     MockTour.add_user(self.test_user)
    #
    #     # Fetch the tour
    #     tour_class = Tour.objects.get_for_user(self.test_user)
    #
    #     urls = tour_class.get_url_list()
    #     expected_urls = ['mock1', 'mock3', 'mock4', 'mock2']
    #     self.assertEqual(expected_urls, urls)
    #
    # def test_next_url(self):
    #     """
    #     Verifies that the tour manager's next url method works
    #     """
    #     self.assertIsNone(Tour.objects.get_next_url(self.test_user))
    #     MockTour.add_user(self.test_user)
    #     self.assertEqual('mock1', Tour.objects.get_next_url(self.test_user))
    #
    # def test_updates(self):
    #     """
    #     Verifies that when tour or step data are updated, their records get updated as well.
    #     Also verifies that when steps of a tour change, the db reflects that
    #     """
    #     # create tour and add user
    #     MockTour.add_user(self.test_user)
    #
    #     # change the name
    #     MockTour.name = 'Changed Tour Name'
    #
    #     # fetch the tour like it is going to be displayed
    #     tour_class = Tour.objects.get_for_user(self.test_user)
    #
    #     # the tour name should have been changed
    #     self.assertEqual(tour_class.tour.name, MockTour.name)
    #
    #     # change a step name
    #     MockStep1.name = 'Changed Step Name'
    #     with patch('tour.tests.mocks.MockStep1.get_url') as mock_get_url:
    #         mock_get_url.return_value = 'different_url'
    #
    #         # load the tour
    #         tour_class = Tour.objects.get_for_user(self.test_user)
    #         self.assertEqual(tour_class.current_step_class.step.name, MockStep1.name)
    #         self.assertEqual(tour_class.current_step_class.step.url, MockStep1.get_url())
