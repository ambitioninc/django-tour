from django.contrib.auth.models import User
from django.template import Template, Context
from tour.tests.mocks import MockTour, MockRequest, MockStep1
from tour.tests.tour_tests import BaseTourTest


class TourTest(BaseTourTest):

    def test_tour_tag(self):
        """
        Verifies that a tour gets displayed when a user has a tour
        """
        # Verifies that the tour template does not get rendered without a user
        MockTour.create()
        test_template = Template('{% load tour_tags %}{% tour_navigation %}')
        context = Context({
            'request': MockRequest(User(), '/mock/path'),
        })
        self.assertEqual('', test_template.render(context))

        # Verifies that the tour template does not get rendered if a user doesn't have a tour
        self.login_user1()
        context = Context({
            'request': MockRequest(self.test_user, '/mock/path'),
        })
        self.assertEqual('', test_template.render(context).strip())

        # Verifies that the tour template does get rendered if a user has a tour
        MockTour.add_user(self.test_user)
        test_template = Template('{% load tour_tags %}{% tour_navigation %}')
        context = Context({
            'request': MockRequest(self.test_user, '/mock/path'),
        })
        self.assertTrue('tour-wrap' in test_template.render(context))

        # Verify that the current class gets applied
        context = Context({
            'request': MockRequest(self.test_user, 'mock1'),
        })
        self.assertTrue('current' in test_template.render(context))

        # Verify that the complete class gets applied
        MockStep1.complete = True
        context = Context({
            'request': MockRequest(self.test_user, 'mock2'),
        })
        self.assertTrue('complete' in test_template.render(context))

        # Verify no errors for missing request object
        context = Context({})
        self.assertEqual('', test_template.render(context))
