from django.contrib.auth.models import User
from django.test import TestCase
from django_dynamic_fixture import G
from mock import patch

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
        self.step5 = G(
            Step, step_class='tour.tours.BaseStep', display_name='Mock Step 5', name='mock5',
            url=None, parent_step=None, sort_order=4)

    def login_user1(self):
        self.client.login(username='test', password='test')


class TourTest(BaseTourTest):
    """
    Tests the functionality of the BaseTour class
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
        self.tour1.steps.add(self.step1, self.step5, self.step2)
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

    @patch('tour.tests.mocks.MockStep4.is_complete', spec_set=True)
    @patch('tour.tests.mocks.MockStep3.is_complete', spec_set=True)
    @patch('tour.tests.mocks.MockStep2.is_complete', spec_set=True)
    @patch('tour.tests.mocks.MockStep1.is_complete', spec_set=True)
    def test_get_current_step(
            self, mock_step1_is_complete, mock_step2_is_complete, mock_step3_is_complete, mock_step4_is_complete):
        """
        Verifies that the tour class returns the first incomplete step
        :type mock_step1_is_complete: Mock
        :type mock_step2_is_complete: Mock
        :type mock_step3_is_complete: Mock
        :type mock_step4_is_complete: Mock
        """
        mock_step1_is_complete.return_value = False
        mock_step2_is_complete.return_value = False
        mock_step3_is_complete.return_value = False
        mock_step4_is_complete.return_value = False

        self.tour1.steps.add(self.step1, self.step2)
        self.step1.steps.add(self.step3, self.step4)
        tour1_class = self.tour1.load_tour_class()

        self.assertEqual(self.step1, tour1_class.get_current_step(self.test_user))

        mock_step1_is_complete.return_value = True
        mock_step3_is_complete.return_value = True
        self.assertEqual(self.step4, tour1_class.get_current_step(self.test_user))

        mock_step4_is_complete.return_value = True
        mock_step2_is_complete.return_value = True
        self.assertIsNone(tour1_class.get_current_step(self.test_user))

    @patch('tour.tests.mocks.MockStep4.is_complete', spec_set=True)
    @patch('tour.tests.mocks.MockStep3.is_complete', spec_set=True)
    @patch('tour.tests.mocks.MockStep2.is_complete', spec_set=True)
    @patch('tour.tests.mocks.MockStep1.is_complete', spec_set=True)
    def test_get_next_url(
            self, mock_step1_is_complete, mock_step2_is_complete, mock_step3_is_complete, mock_step4_is_complete):
        """
        Verifies that the url is returned for the current step
        :type mock_step1_is_complete: Mock
        :type mock_step2_is_complete: Mock
        :type mock_step3_is_complete: Mock
        :type mock_step4_is_complete: Mock
        """
        mock_step1_is_complete.return_value = False
        mock_step2_is_complete.return_value = False
        mock_step3_is_complete.return_value = False
        mock_step4_is_complete.return_value = False

        self.step5.sort_order = 1
        self.step5.save()
        self.step2.sort_order = 3
        self.step2.save()

        self.tour1.steps.add(self.step1, self.step2, self.step5)
        self.step5.steps.add(self.step3, self.step4)
        tour1_class = self.tour1.load_tour_class()

        self.assertEqual('mock1', tour1_class.get_next_url(self.test_user))

        mock_step1_is_complete.return_value = True
        self.assertEqual('mock3', tour1_class.get_next_url(self.test_user))

        mock_step3_is_complete.return_value = True
        self.assertEqual('mock4', tour1_class.get_next_url(self.test_user))

        mock_step4_is_complete.return_value = True
        self.assertEqual('mock2', tour1_class.get_next_url(self.test_user))

        mock_step2_is_complete.return_value = True
        self.assertEqual('mock_complete1', tour1_class.get_next_url(self.test_user))

    @patch('tour.tests.mocks.MockStep1.is_complete', spec_set=True)
    def test_is_complete(self, mock_step1_is_complete):
        """
        Verifies that a tour returns true when complete and false when incomplete
        :type mock_step1_is_complete: Mock
        """
        mock_step1_is_complete.return_value = False

        self.tour1.steps.add(self.step1)
        tour1_class = self.tour1.load_tour_class()

        self.assertFalse(tour1_class.is_complete(self.test_user))

        mock_step1_is_complete.return_value = True
        self.assertTrue(tour1_class.is_complete(self.test_user))


class StepTest(BaseTourTest):
    """
    Tests the functionality of the BaseStep class
    """
    def test_init(self):
        """
        Verifies that the step object is properly set when loaded
        """
        self.assertEqual(self.step1.load_step_class().step, self.step1)

    def test_is_complete(self):
        """
        Verifies that a step returns true by default
        """
        step1_class = self.step1.load_step_class()
        self.assertTrue(step1_class.is_complete(self.test_user))

    def test_get_steps_flat(self):
        """
        Verifies that the steps are loaded in the correct order
        """
        self.step1.steps.add(self.step2, self.step3)
        expected_steps = [self.step2, self.step3]
        self.assertEqual(expected_steps, self.step1.load_step_class().get_steps())

    def test_get_steps_nested(self):
        """
        Verifies that the nested steps are loaded correctly
        """
        self.step1.steps.add(self.step2)
        self.step2.steps.add(self.step3, self.step4)
        expected_steps = [self.step2, self.step3, self.step4]
        self.assertEqual(expected_steps, self.step1.load_step_class().get_steps())
