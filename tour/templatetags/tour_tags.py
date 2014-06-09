from copy import deepcopy
import json

from django import template
from django.template.loader import get_template

from tour.api import TourResource
from tour.models import Tour
from tour.serializers import TourSerializer


register = template.Library()


class TourNavNode(template.Node):
    def __init__(self, always_show=False):
        self.always_show = always_show

    def get_tour(self, request):
        # Check for any tours
        tour = Tour.objects.get_for_user(request.user)

        if not tour and self.always_show:
            tour = Tour.objects.get_recent_tour(request.user)
        if self.always_show:
            mutable_get = deepcopy(request.GET)
            mutable_get['always_show'] = True
            request.GET = mutable_get
        return tour

    def add_display_data(self, tour_dict, request):
        if not tour_dict:
            return None

        # Set the step css classes
        previous_steps_complete = True
        is_after_current = False
        for step_dict in tour_dict['steps']:
            classes = []
            if step_dict['url'] == request.path:
                classes.append('current')
                step_dict['current'] = True
                tour_dict['display_name'] = step_dict['name']
                is_after_current = True
            if not previous_steps_complete:
                classes.append('incomplete')
                classes.append('unavailable')
                step_dict['url'] = '#'
            elif not step_dict['complete']:
                classes.append('incomplete')
                classes.append('available')
                previous_steps_complete = False
            elif is_after_current:
                classes.append('available')
            else:
                classes.append('complete')
                classes.append('available')
            step_dict['cls'] = ' '.join(classes)

        return tour_dict

    def render(self, context):
        if 'request' in context and hasattr(context['request'], 'user'):
            # Make sure this isn't the anonymous user
            if not context['request'].user.id:
                return ''

            tour = self.get_tour(context['request'])
            context['tour'] = self.add_display_data(TourSerializer(tour).data, context['request'])

            # Load the tour template and render it
            tour_template = get_template('tour/tour_navigation.html')
            return tour_template.render(context)
        return ''


@register.simple_tag(takes_context=True)
def tour_navigation(context, **kwargs):
    """
    Tag to render the tour nav node
    """
    return TourNavNode(always_show=kwargs.get('always_show', False)).render(context)
