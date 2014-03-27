from django.conf.urls import patterns, include, url
from tastypie.api import NamespacedApi

from .api import TourResource, StepResource

api = NamespacedApi(api_name='api', urlconf_namespace='tour')
api.register(TourResource())
api.register(StepResource())

urlpatterns = patterns(
    '',
    url(r'^', include(api.urls, namespace='tour')),
)
