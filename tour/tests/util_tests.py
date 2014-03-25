from django.test import TestCase
from tour.utils.import_string import import_string


class UtilTest(TestCase):

    def test_import_string(self):
        """
        Tests all outcomes out import_string
        """
        # Make sure an invalid module path returns None
        self.assertIsNone(import_string('nope.nope'))

        # Make sure an invalid module name returns None
        self.assertIsNone(import_string('tour.nope'))

        # For test coverage, import a null value
        self.assertIsNone(import_string('tour.tests.mocks.mock_null_value'))
