from tour.serializers import TourSerializer, StepSerializer
from tour.tests.tour_tests import BaseTourTest


class SerializerTest(BaseTourTest):
    """
    Tests the serializers contained in the tour app
    """
    def test_step_serializer(self):
        """
        Tests the Step model serialization
        """
        self.tour1.steps.add(self.step1, self.step2)
        self.step1.steps.add(self.step3, self.step4)
        self.assertEqual(StepSerializer(self.step1).data, {
            'name': 'mock1',
            'display_name': 'Mock Step 1',
            'url': 'mock1',
            'sort_order': 0,
            'complete': False,
            'steps': [{
                'name': 'mock3',
                'display_name': 'Mock Step 3',
                'url': 'mock3',
                'sort_order': 2,
                'steps': [],
                'complete': False,
            }, {
                'name': 'mock4',
                'display_name': 'Mock Step 4',
                'url': 'mock4',
                'sort_order': 3,
                'steps': [],
                'complete': False,
            }]
        })

    def test_tour_serializer(self):
        """
        Tests the Tour model serialization
        """
        self.tour1.steps.add(self.step1, self.step2)
        self.step1.steps.add(self.step3, self.step4)
        self.assertEqual(TourSerializer(self.tour1).data, {
            'name': 'tour1',
            'display_name': 'Mock Tour',
            'complete_url': 'mock_complete1',
            'steps': [{
                'name': 'mock1',
                'display_name': 'Mock Step 1',
                'url': 'mock1',
                'sort_order': 0,
                'complete': False,
                'steps': [{
                    'name': 'mock3',
                    'display_name': 'Mock Step 3',
                    'url': 'mock3',
                    'sort_order': 2,
                    'steps': [],
                    'complete': False,
                }, {
                    'name': 'mock4',
                    'display_name': 'Mock Step 4',
                    'url': 'mock4',
                    'sort_order': 3,
                    'steps': [],
                    'complete': False,
                }]
            }, {
                'name': 'mock2',
                'display_name': 'Mock Step 2',
                'url': 'mock2',
                'sort_order': 1,
                'steps': [],
                'complete': False,
            }]
        })
