from django.core.urlresolvers import reverse
import json
from tour.tests.mocks import MockTour, MockStep1, MockStep2

from tour.tests.tour_tests import BaseTourTest


class ApiTest(BaseTourTest):

    def login_user1(self):
        self.client.login(username='test', password='test')

    def login_user2(self):
        self.client.login(username='test2', password='test2')

    def test_fetch_tour(self):
        self.login_user1()
        url = reverse('tour:api_dispatch_list', kwargs={'resource_name': 'tour', 'api_name': 'api'})
        MockTour.create()

        # Make sure there are no tour objects returned
        response = self.client.get(url)
        self.assertEqual(200, response.status_code)
        json_response = json.loads(response.content)
        objects = json_response.get('objects')
        self.assertEqual(0, len(objects))

        # Make sure there is one tour object returned
        MockTour.add_user(self.test_user)
        response = self.client.get(url)
        self.assertEqual(200, response.status_code)
        json_response = json.loads(response.content)
        objects = json_response.get('objects')
        self.assertEqual(1, len(objects))

        # Create a tour for a second user and make sure only the one tour is returned
        MockTour.add_user(self.test_user2)
        response = self.client.get(url)
        self.assertEqual(200, response.status_code)
        json_response = json.loads(response.content)
        objects = json_response.get('objects')
        self.assertEqual(1, len(objects))

        # Complete the tour for user 1
        MockStep1.complete = True
        MockStep2.complete = True
        response = self.client.get(url)
        self.assertEqual(200, response.status_code)
        json_response = json.loads(response.content)
        objects = json_response.get('objects')
        self.assertEqual(0, len(objects))

        # Log in as user 2 and make sure there is still a tour
        self.login_user2()
        MockStep1.complete = False
        MockStep2.complete = False
        response = self.client.get(url)
        self.assertEqual(200, response.status_code)
        json_response = json.loads(response.content)
        objects = json_response.get('objects')
        self.assertEqual(1, len(objects))
