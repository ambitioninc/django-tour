from django.contrib.auth.models import User
from django.template import Template, Context
from mock import Mock

from tour.tests.tour_tests import BaseTourTest


class TemplateTagTest(BaseTourTest):
    """
    Tests the functionality of the template tag
    """

    def setUp(self):
        super(TemplateTagTest, self).setUp()
        self.test_template = Template('{% load tour_tags %}{% tour_navigation %}')

    def test_template_no_user(self):
        """
        Verifies that the tour template does not get rendered without a user
        """
        context = Context({
            'request': Mock(
                user=User(),
                path='/mock/path',
                method='get',
                GET={},
            ),
        })
        self.assertEqual('', self.test_template.render(context))

    def test_tour_tag(self):
        """

        """

        # Verifies that the tour template does not get rendered if a user doesn't have a tour
        self.login_user1()
        context = Context({
            'request': Mock(
                user=self.test_user,
                path='/mock/path',
                method='get',
                GET={},
            ),
        })
        self.assertEqual('', self.test_template.render(context).strip())

        # Verifies that the tour template gets rendered if a user has a tour
        self.tour1.load_tour_class().add_user(self.test_user)
        context = Context({
            'request': Mock(
                user=self.test_user,
                path='/mock/path',
                method='get',
                GET={},
            ),
        })
        self.assertTrue('tour-wrap' in self.test_template.render(context))

        # Verify that the current class gets applied
        context = Context({
            'request': Mock(
                user=self.test_user,
                path='mock1',
                method='get',
                GET={},
            ),
        })
        self.assertTrue('current' in self.test_template.render(context))

        # Verify that the complete class gets applied
        MockStep1.complete = True
        context = Context({
            'request': MockRequest(self.test_user, 'mock2'),
        })
        self.assertTrue('complete' in self.test_template.render(context))

        # Make sure no tour gets rendered when it is complete
        MockStep2.complete = True
        context = Context({
            'request': Mock(
                user=self.test_user,
                path='/mock/path',
                method='get',
                GET={},
            ),
        })
        self.assertTrue('tour-wrap' not in self.test_template.render(context))

        # Makes sure that the tour does get displayed if the always_show flag is on
        self.test_template = Template('{% load tour_tags %}{% tour_navigation always_show=True %}')
        context = Context({
            'request': Mock(
                user=self.test_user,
                path='/mock/path',
                method='get',
                GET={},
            ),
        })
        self.assertTrue('tour-wrap' in self.test_template.render(context))

        # Verify no errors for missing request object
        context = Context({})
        self.assertEqual('', self.test_template.render(context))

    def test_step_classes(self):
        self.login_user1()
        self.tour1.load_tour_class().add_user(self.test_user)

        # Test that the second step has an available class but not a complete class
        MockStep1.complete = True
        MockStep2.complete = True
        self.test_template = Template('{% load tour_tags %}{% tour_navigation always_show=True %}')
        context = Context({
            'request': MockRequest(self.test_user, 'mock1'),
        })
        rendered_content = self.render_and_clean(self.test_template, context)
        expected_str = '<a href="mock2" class="step-circle available ">'
        self.assertTrue(expected_str in rendered_content)

    def test_tour_title(self):
        """
        Makes sure the appropriate title gets displayed for the tour title
        """
        self.login_user1()
        self.tour1.load_tour_class().add_user(self.test_user)

        self.test_template = Template('{% load tour_tags %}{% tour_navigation %}')
        context = Context({
            'request': Mock(
                user=self.test_user,
                path='mock1',
                method='get',
                GET={},
            ),
        })
        rendered_content = self.render_and_clean(self.test_template, context)

        # Make sure the current step is displayed
        expected_html = '<div class="tour-name">{0}</div>'.format(MockStep1.name)
        self.assertTrue(expected_html in rendered_content)

        # Make sure the tour title is displayed
        context = Context({
            'request': Mock(
                user=self.test_user,
                path='mock0',
                method='get',
                GET={},
            ),
        })
        rendered_content = self.render_and_clean(self.test_template, context)
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
