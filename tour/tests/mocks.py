from django.http import HttpResponse
from django.views.generic import View
from tour.tours import BaseStep, BaseTour
from tour.views import TourStepMixin


mock_null_value = None


class MockView(TourStepMixin, View):
    def get(self, request):
        return HttpResponse('ok')


class MockRequest(object):
    def __init__(self, user=None, path=None, params=None, method=None):
        self.user = user
        self.path = path
        self.method = method or 'get'
        self.GET = params or {}


class MockStep1(BaseStep):
    pass


class MockStep2(BaseStep):
    pass


class MockStep3(BaseStep):
    pass


class MockStep4(BaseStep):
    pass


class EmptyStep(BaseStep):
    pass


class NoUrlStep(BaseStep):
    step_class = 'tour.tests.mocks.NoUrlStep'
    name = 'No Url Step'
    complete = False


class MockTour(BaseTour):
    pass


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
