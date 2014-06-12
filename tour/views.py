from django.http import HttpResponseRedirect
from tour.models import Tour


class TourStepMixin(object):
    """
    Provides a method for requiring navigation through the tour steps in order
    """
    def tour_should_redirect(self, user, tour_class, current_index, next_index):
        # check if tour is incomplete
        if tour_class.get_current_step(user):
            # check if the current step is later in the tour than the expected step
            if current_index >= 0 and next_index >= 0:
                if current_index > next_index:
                    return True
        else:
            # tour is complete, make sure we don't go backwards
            # check that the current page is a step of the tour and check if the current page
            # is the next page of the tour (which should be the last page)
            if current_index >= 0 and current_index != next_index:
                return True
        return False

    def get_user_tour(self, request):
        # Get the tour class for the user
        tour = Tour.objects.get_for_user(request.user)
        if tour is None:
            tour = Tour.objects.get_recent_tour(request.user)
        return tour

    def get_tour_redirect_url(self, request):
        tour = self.get_user_tour(request)
        if not tour:
            return None

        # Determine the current step and expected step indices
        tour_class = tour.load_tour_class()
        next_url = tour_class.get_next_url(request.user)
        url_list = tour_class.get_url_list()

        current_index = -1
        next_index = -1
        if request.path in url_list:
            current_index = url_list.index(request.path)
        if next_url in url_list:
            next_index = url_list.index(next_url)
        should_redirct = self.tour_should_redirect(request.user, tour_class, current_index, next_index)
        if should_redirct:
            return next_url
        return None

    def dispatch(self, request, *args, **kwargs):
        redirect_url = self.get_tour_redirect_url(request)
        if redirect_url:
            return HttpResponseRedirect(redirect_url)

        return super(TourStepMixin, self).dispatch(request, *args, **kwargs)
