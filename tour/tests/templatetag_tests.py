from django.contrib.auth.models import User
from django.template import Template, Context
from tour.tests.mocks import MockTour, MockRequest, MockStep1, MockStep2
from tour.tests.tour_tests import BaseTourTest


class TemplateTagTest(BaseTourTest):
    """
    Tests the functionality of the template tag
    """
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

        # Verifies that the tour template gets rendered if a user has a tour
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

        # Make sure no tour gets rendered when it is complete
        MockStep2.complete = True
        test_template = Template('{% load tour_tags %}{% tour_navigation %}')
        context = Context({
            'request': MockRequest(self.test_user, '/mock/path'),
        })
        self.assertTrue('tour-wrap' not in test_template.render(context))

        # Makes sure that the tour does get displayed if the always_show flag is on
        test_template = Template('{% load tour_tags %}{% tour_navigation always_show=True %}')
        context = Context({
            'request': MockRequest(self.test_user, '/mock/path'),
        })
        self.assertTrue('tour-wrap' in test_template.render(context))

        # Verify no errors for missing request object
        context = Context({})
        self.assertEqual('', test_template.render(context))

    def test_tour_title(self):
        """
        Makes sure the appropriate title gets displayed for the tour title
        """
        self.login_user1()
        MockTour.add_user(self.test_user)

        test_template = Template('{% load tour_tags %}{% tour_navigation %}')
        context = Context({
            'request': MockRequest(self.test_user, 'mock1'),
        })
        rendered_content = self.render_and_clean(test_template, context)

        # Make sure the current step is displayed
        expected_html = '<div class="tour-name">{0}</div>'.format(MockStep1.name)
        self.assertTrue(expected_html in rendered_content)

        # Make sure the tour title is displayed
        context = Context({
            'request': MockRequest(self.test_user, 'mock0'),
        })
        rendered_content = self.render_and_clean(test_template, context)
        expected_html = '<div class="tour-name">{0}</div>'.format(MockTour.name)
        self.assertTrue(expected_html in rendered_content)

    def render_and_clean(self, template, context):
        # render the template
        rendered_content = template.render(context).strip()
        # remove tabs
        rendered_content = rendered_content.replace('    ', '')
        # remove new lines
        rendered_content = rendered_content.replace('\n', '')
        return rendered_content
