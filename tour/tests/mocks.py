from django.views.generic import View
from tour.tours import BaseStep, BaseTour
from tour.views import TourStepMixin


mock_null_value = None


class MockView(TourStepMixin, View):
    pass


class MockRequest(object):
    def __init__(self, user=None, path=None, params=None, method=None):
        self.user = user
        self.path = path
        self.method = method or 'get'
        self.GET = params or {}


class MockStep(BaseStep):
    complete = False

    def is_complete(self, user=None):
        return self.complete


class MockStep1(MockStep):
    step_class = 'tour.tests.mocks.MockStep1'
    name = 'Mock Step 1'
    complete = False

    @classmethod
    def get_url(cls):
        return 'mock1'


class MockStep2(MockStep):
    step_class = 'tour.tests.mocks.MockStep2'
    name = 'Mock Step 2'
    complete = False

    @classmethod
    def get_url(cls):
        return 'mock2'


class MockStep3(MockStep):
    step_class = 'tour.tests.mocks.MockStep3'
    name = 'Mock Step 3'
    complete = False
    parent_step = MockStep1

    @classmethod
    def get_url(cls):
        return 'mock3'


class MockStep4(MockStep):
    step_class = 'tour.tests.mocks.MockStep4'
    name = 'Mock Step 4'
    complete = False
    parent_step = MockStep1

    @classmethod
    def get_url(cls):
        return 'mock4'


class EmptyStep(MockStep):
    pass


class NoUrlStep(MockStep):
    step_class = 'tour.tests.mocks.NoUrlStep'
    name = 'No Url Step'
    complete = False


class MockTour(BaseTour):
    tour_class = 'tour.tests.mocks.MockTour'
    name = 'Mock Tour'
    complete_url = 'mock_complete1'
    steps = [
        MockStep1,
        MockStep2,
    ]


class MockTour2(BaseTour):
    tour_class = 'tour.tests.mocks.MockTour2'
    name = 'Mock Tour 2'
    complete_url = 'mock_complete2'
    parent_tour = MockTour
    steps = [
        MockStep3,
        MockStep4,
    ]


class MockTour3(BaseTour):
    tour_class = 'tour.tests.mocks.MockTour3'
    name = 'Mock Tour 3'
    complete_url = 'mock_complete3'
    steps = [
        EmptyStep
    ]


class MockTour4(BaseTour):
    name = 'Mock Tour 4'
    complete_url = 'mock_complete4'
    steps = [
        EmptyStep
    ]


class CompleteTour(BaseTour):
    tour_class = 'tour.tests.mocks.CompleteTour'
    name = 'Complete Tour'
    complete_url = 'mock_complete'
    steps = [
        MockStep1
    ]

    def is_complete(self, user=None):
        return True
