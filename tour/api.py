from rest_framework.authentication import SessionAuthentication
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from tour.filters import TourFilter
from tour.models import Tour
from tour.serializers import TourSerializer


class TourApiView(ListAPIView):
    serializer_class = TourSerializer
    filter_class = TourFilter
    permission_classes = (IsAuthenticated,)
    authentication_classes = (SessionAuthentication,)

    def get_queryset(self):
        Tour.objects.complete_tours(self.request.user)
        return Tour.objects.filter(tourstatus__user=self.request.user, tourstatus__complete=False)
