from mock import Mock, patch
from tour.tests.mocks import MockView
from tour.tests.tour_tests import BaseTourTest


class ViewTest(BaseTourTest):
    """
    Tests the functionality of all tour views and mixins
    """
    def setUp(self):
        super(ViewTest, self).setUp()
        self.tour1.steps.add(self.step1, self.step2, self.step3)

    def test_no_tour(self):
        """
        Verify that the user isn't redirected with no tour
        """
        mock_request = Mock(user=self.test_user, path='mock2', method='get', GET={})
        mock_view = MockView(request=mock_request)
        response = mock_view.dispatch(mock_request)
        self.assertEqual(200, response.status_code)

    @patch('tour.tests.mocks.MockStep1.is_complete', spec_set=True)
    def test_request_unrelated_page(self, mock_step1_is_complete):
        """
        Verifies that user can go to a non-tour page
        :type mock_step1_is_complete: Mock
        """
        mock_step1_is_complete.return_value = False

        self.tour1.load_tour_class().add_user(self.test_user)

        # request page that isn't in the tour before tour is complete
        mock_request = Mock(user=self.test_user, path='mock-fake', method='get', GET={})
        mock_view = MockView(request=mock_request)
        response = mock_view.dispatch(mock_request)
        self.assertEqual(200, response.status_code)

    @patch('tour.tests.mocks.MockStep1.is_complete', spec_set=True)
    def test_request_first_step(self, mock_step1_is_complete):
        """
        Request the first step of the tour and verify that the page is accessible
        :type mock_step1_is_complete: Mock
        """
        mock_step1_is_complete.return_value = False

        self.tour1.load_tour_class().add_user(self.test_user)
        mock_request = Mock(user=self.test_user, path='mock1', method='get', GET={})
        mock_view = MockView(request=mock_request)
        response = mock_view.dispatch(mock_request)
        self.assertEqual(200, response.status_code)

    @patch('tour.tests.mocks.MockStep1.is_complete', spec_set=True)
    def test_redirect_from_future_step(self, mock_step1_is_complete):
        """
        Try to access the second step of the tour before the first is complete. The user should be
        redirected to the first step
        :type mock_step1_is_complete: Mock
        """
        mock_step1_is_complete.return_value = False

        # do request to second step when we should be on first
        self.tour1.load_tour_class().add_user(self.test_user)
        mock_request = Mock(user=self.test_user, path='mock2', method='get', GET={})
        mock_view = MockView(request=mock_request)
        response = mock_view.dispatch(mock_request)
        self.assertEqual(302, response.status_code)
        self.assertEqual('mock1', response.url)

    def test_tour_complete_url_redirect(self):
        """
        Verifies that a user can't go to steps out of order and can't go to other steps
        after the tour is complete
        """
        # complete tour and try to go to first step
        self.tour1.load_tour_class().add_user(self.test_user)
        mock_request = Mock(user=self.test_user, path='mock1', method='get', GET={})
        mock_view = MockView(request=mock_request)
        response = mock_view.dispatch(mock_request)
        self.assertEqual(302, response.status_code)
        self.assertEqual('mock_complete1', response.url)

    def test_tour_complete_unrelated_page(self):
        """
        Verifies that the user can access a non-tour page after finishing a tour
        """
        # request page that isn't in the tour when tour is complete
        self.tour1.load_tour_class().add_user(self.test_user)
        mock_request = Mock(user=self.test_user, path='mock-fake', method='get', GET={})
        mock_view = MockView(request=mock_request)
        response = mock_view.dispatch(mock_request)
        self.assertEqual(200, response.status_code)
