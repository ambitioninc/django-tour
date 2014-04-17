from django.http import HttpResponseRedirect
from tour.models import Tour


class TourStepMixin(object):
    """
    Provides a method for requiring navigation through the tour steps in order
    """
    def dispatch(self, request, *args, **kwargs):
        # Get the tour class for the user
        tour_class = Tour.objects.get_for_user(request.user)
        if tour_class is None:
            tour_class = Tour.objects.get_recent_tour(request.user)
        if not tour_class:
            return super(TourStepMixin, self).dispatch(request, *args, **kwargs)

        # Determine the current step and expected step indices
        next_url = tour_class.get_next_url()
        url_list = tour_class.get_url_list()
        current_index = -1
        next_index = -1
        if request.path in url_list:
            current_index = url_list.index(request.path)
        if next_url in url_list:
            next_index = url_list.index(next_url)

        # check if tour is incomplete
        if tour_class.current_step_class:
            # check if the current step is later in the tour than the expected step
            if current_index >= 0 and next_index >= 0:
                if current_index > next_index:
                    return HttpResponseRedirect(next_url)
        else:
            # tour is complete, make sure we don't go backwards
            # check that the current page is a step of the tour and check if the current page
            # is the next page of the tour (which should be the last page)
            if current_index >= 0 and current_index != next_index:
                return HttpResponseRedirect(next_url)

        return super(TourStepMixin, self).dispatch(request, *args, **kwargs)
