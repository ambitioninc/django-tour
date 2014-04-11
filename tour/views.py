from django.http import HttpResponseRedirect
from tour.models import Tour


class TourStepMixin(object):
    require_step_order = True

    def dispatch(self, request, *args, **kwargs):
        tour_class = Tour.objects.get_for_user(request.user)
        next_url = tour_class.get_next_url()
        url_list = tour_class.get_url_list()
        current_index = -1
        next_index = -1
        if request.path in url_list:
            current_index = url_list.index(request.path)
        if next_url in url_list:
            next_index = url_list.index(next_url)
        if current_index >= 0 and next_index >= 0:
            if current_index > next_index:
                return HttpResponseRedirect(next_url)

        return super(TourStepMixin, self).dispatch(request, *args, **kwargs)
