"""
Custom template tags for displaying tour navigation
"""
from django import template
from django.template import Template
from django.template.loader import get_template
from django.utils.html import escape
import json
from pprint import pprint
from tour.api import TourResource
from tour.models import Tour


register = template.Library()


@register.tag
def tour_navigation(parser, token):
    """
    Creates a hidden field for EXT that contains a serialized json object of the authenticated account.
    """
    return TourNavigationNode()


class TourNavigationNode(template.Node):
    """
    The rendering code for the ext_auth_account tag.
    """
    def render(self, context):
        if 'request' in context and hasattr(context['request'], 'user'):
            # Check for any tours
            tour_class = Tour.objects.get_for_user(context['request'].user)

            # Add tour to the template if it exists
            if tour_class:
                # Serialize the tour and its steps
                tour = tour_class.tour
                tour_resource = TourResource()
                tour_bundle = tour_resource.build_bundle(obj=tour, request=context['request'])
                tour_data = tour_resource.full_dehydrate(tour_bundle)
                tour_json = tour_resource.serialize(None, tour_data, 'application/json')
                tour_dict = json.loads(tour_json)

                # Determine the highest completed step

                # Set the step css classes
                previous_steps_complete = True
                for step_dict in tour_dict['steps']:
                    cls = 'complete'
                    if step_dict['url'] in context['request'].path:
                        cls = 'current'
                    elif not step_dict['complete'] or not previous_steps_complete:
                        cls = 'incomplete'
                        previous_steps_complete = False
                    step_dict['cls'] = cls

                context['tour'] = tour_dict

            # Load the tour template and render it
            tour_template = get_template('tour/tour_navigation.html')
            return tour_template.render(context)
