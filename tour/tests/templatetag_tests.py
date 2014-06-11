from django.contrib.auth.models import User
from django.template import Template, Context
from mock import Mock, patch

from tour.tests.tour_tests import BaseTourTest


class TemplateTagTest(BaseTourTest):
    """
    Tests the functionality of the template tag
    """

    def setUp(self):
        super(TemplateTagTest, self).setUp()
        self.test_template = Template('{% load tour_tags %}{% tour_navigation %}')
        self.tour1.steps.add(self.step1, self.step2, self.step3, self.step4)

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

    def test_template_no_tour(self):
        """
        Verifies that the tour template does not get rendered if a user doesn't have a tour
        """
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

    @patch('tour.tests.mocks.MockStep1.is_complete', spec_set=True)
    def test_user_with_tour(self, mock_step1_is_complete):
        """
        Verifies that the tour template gets rendered if a user has a tour
        :type mock_step1_is_complete: Mock
        """
        mock_step1_is_complete.return_value = False

        self.login_user1()
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

    @patch('tour.tests.mocks.MockStep1.is_complete', spec_set=True)
    def test_current_class(self, mock_step1_is_complete):
        """
        Verify that the current class gets applied
        :type mock_step1_is_complete: Mock
        """
        mock_step1_is_complete.return_value = False

        self.login_user1()
        self.tour1.load_tour_class().add_user(self.test_user)
        context = Context({
            'request': Mock(
                user=self.test_user,
                path='mock1',
                method='get',
                GET={},
            ),
        })
        self.assertTrue('current' in self.test_template.render(context))

    @patch('tour.tests.mocks.MockStep2.is_complete', spec_set=True)
    def test_complete_class(self, mock_step2_is_complete):
        """
        Verify that the complete class gets applied
        :type mock_step2_is_complete: Mock
        """
        mock_step2_is_complete.return_value = False

        self.login_user1()
        self.tour1.load_tour_class().add_user(self.test_user)
        context = Context({
            'request': Mock(
                user=self.test_user,
                path='/mock/path',
                method='get',
                GET={},
            ),
        })
        self.assertTrue('complete' in self.test_template.render(context))

    def test_complete_tour(self):
        """
        Make sure no tour gets rendered when it is complete
        """
        self.login_user1()
        self.tour1.load_tour_class().add_user(self.test_user)
        context = Context({
            'request': Mock(
                user=self.test_user,
                path='/mock/path',
                method='get',
                GET={},
            ),
        })
        self.assertTrue('tour-wrap' not in self.test_template.render(context))

    def test_always_display(self):
        """
        Makes sure that the tour does get displayed if the always_show flag is on
        """
        self.test_template = Template('{% load tour_tags %}{% tour_navigation always_show=True %}')

        self.login_user1()
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

    def test_missing_request(self):
        """
        Verify no errors for missing request object
        """
        context = Context({})
        self.assertEqual('', self.test_template.render(context))

    @patch('tour.tests.mocks.MockStep2.is_complete', spec_set=True)
    @patch('tour.tests.mocks.MockStep1.is_complete', spec_set=True)
    def test_step_classes(self, mock_step1_is_complete, mock_step2_is_complete):
        """
        Test that the second step has an available class but not a complete class
        :type mock_step1_is_complete: Mock
        :type mock_step2_is_complete: Mock
        """
        mock_step1_is_complete.return_value = True
        mock_step2_is_complete.return_value = False
        self.test_template = Template('{% load tour_tags %}{% tour_navigation always_show=True %}')

        self.login_user1()
        self.tour1.load_tour_class().add_user(self.test_user)
        context = Context({
            'request': Mock(
                user=self.test_user,
                path='/mock/path',
                method='get',
                GET={},
            ),
        })
        rendered_content = self.render_and_clean(self.test_template, context)

        # test incomplete unavailable
        expected_str = '<a href="#" class="step-circle incomplete unavailable">'
        self.assertTrue(expected_str in rendered_content)

        # test incomplete available
        expected_str = '<a href="mock2" class="step-circle incomplete available">'
        self.assertTrue(expected_str in rendered_content)

        # complete the second step
        mock_step2_is_complete.return_value = True

        # request the first page
        context = Context({
            'request': Mock(
                user=self.test_user,
                path='mock1',
                method='get',
                GET={},
            ),
        })
        rendered_content = self.render_and_clean(self.test_template, context)

        # test available
        expected_str = '<a href="mock2" class="step-circle available">'
        self.assertTrue(expected_str in rendered_content)

        # test current complete available
        expected_str = '<a href="mock1" class="step-circle current available">'
        self.assertTrue(expected_str in rendered_content)

    @patch('tour.tests.mocks.MockStep1.is_complete', spec_set=True)
    def test_step_display_name(self, mock_step1_is_complete):
        """
        Makes sure the appropriate title gets displayed for the tour title
        :type mock_step1_is_complete: Mock
        """
        mock_step1_is_complete.return_value = False

        self.login_user1()
        self.tour1.load_tour_class().add_user(self.test_user)
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
        expected_html = '<div class="tour-name">{0}</div>'.format(self.step1.display_name)
        self.assertTrue(expected_html in rendered_content)

    @patch('tour.tests.mocks.MockStep1.is_complete', spec_set=True)
    def test_tour_display_name(self, mock_step1_is_complete):
        """
        Makes sure the appropriate title gets displayed for the tour title
        :type mock_step1_is_complete: Mock
        """
        mock_step1_is_complete.return_value = False

        self.login_user1()
        self.tour1.load_tour_class().add_user(self.test_user)

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
        expected_html = '<div class="tour-name">{0}</div>'.format(self.tour1.display_name)
        self.assertTrue(expected_html in rendered_content)

    def render_and_clean(self, template, context):
        # render the template
        rendered_content = template.render(context).strip()
        # remove tabs
        rendered_content = rendered_content.replace('    ', '')
        # remove new lines
        rendered_content = rendered_content.replace('\n', '')
        return rendered_content
