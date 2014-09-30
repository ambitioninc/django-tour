from django.conf.urls import patterns, url
from tour import api


urlpatterns = patterns(
    '',
    url(r'^api/tour/$', api.TourApiView.as_view(), name='tour.tour_api'),
)
