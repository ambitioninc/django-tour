from mock import patch
from tour.models import Tour, TourStatus
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


    def test_get_for_user(self):
        """
        Verifies that an incomplete tour class is fetched for a
        """
        pass

    def test_get_for_user_empty(self):
        """
        Verifies that None is returned if no incomplete tours
        """
        pass

    def test_get_recent_tour(self):
        """
        Makes sure that a recently completed tour is returned
        """
        pass

    def test_get_next_url_current_tour(self):
        """
        Verifies that the next url of a tour will be returned
        """
        pass

    def test_get_next_url_recent_tour(self):
        """
        Verifies that the next url of a recent tour will be returned
        """
        pass

    def test_get_next_url_none(self):
        """
        Verifies that None is returned if no tours exist for a user
        """
        pass
