from tour.tests.mocks import MockTour, MockRequest, MockView, MockStep1, MockStep2
from tour.tests.tour_tests import BaseTourTest


class ViewTest(BaseTourTest):
    """
    Tests the functionality of all tour views and mixins
    """
    def test_tour_step_mixin(self):
        """
        Verifies that a user can't go to steps out of order and can't go to other steps
        after the tour is complete
        """
        # do request when there should be no tour
        mock_request = MockRequest(self.test_user, 'mock2', {})
        mock_view = MockView(request=mock_request)
        response = mock_view.dispatch(mock_request)
        self.assertEqual(200, response.status_code)

        MockTour.add_user(self.test_user)

        # do request to second step when we should be on first
        mock_request = MockRequest(self.test_user, 'mock2', {})
        mock_view = MockView(request=mock_request)
        response = mock_view.dispatch(mock_request)
        self.assertEqual(302, response.status_code)
        self.assertEqual('mock1', response.url)

        # complete tour and try to go to first step
        MockStep1.complete = True
        MockStep2.complete = True
        mock_request = MockRequest(self.test_user, 'mock1', {})
        mock_view = MockView(request=mock_request)
        response = mock_view.dispatch(mock_request)
        self.assertEqual(302, response.status_code)
        self.assertEqual('mock_complete1', response.url)

        # request page that isn't in the tour
        mock_request = MockRequest(self.test_user, 'mock-fake', {})
        mock_view = MockView(request=mock_request)
        response = mock_view.dispatch(mock_request)
        self.assertEqual(200, response.status_code)
