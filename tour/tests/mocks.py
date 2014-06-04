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


class MockTour(BaseTour):
    pass


class MockTour2(BaseTour):
    pass
