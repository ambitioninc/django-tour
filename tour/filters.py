import django_filters

from tour.models import Tour


class TourFilter(django_filters.FilterSet):

    class Meta:
        model = Tour
        fields = ('name',)
