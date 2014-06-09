import json

from tastypie.authentication import SessionAuthentication
from tastypie.authorization import Authorization
from tastypie.resources import ModelResource

from .models import Tour, Step


class StepResource(ModelResource):
    """
    Api to access the Step model. Mostly used for serializing the steps in the tour dehydration
    """
    class Meta:
        queryset = Step.objects.all()
        filtering = {
            'id': ['exact'],
        }

        authorization = Authorization()
        authentication = SessionAuthentication()


class TourResource(ModelResource):
    """
    Api to access the Tour models.
    """
    class Meta:
        queryset = Tour.objects.all()
        filtering = {
            'id': ['exact'],
        }

        authorization = Authorization()
        authentication = SessionAuthentication()

    def dehydrate(self, bundle):
        """
        Provides serialization and flattening of the tour's steps
        """
        bundle = super(TourResource, self).dehydrate(bundle)
        if not bundle.request.GET.get('always_show'):
            is_complete = bundle.obj.load_tour_class().is_complete(user=bundle.request.user)
            if is_complete:
                return None
        steps = bundle.obj.load_tour_class().get_steps()
        serialized = []
        step_resource = StepResource()
        for step in steps:
            step_bundle = step_resource.build_bundle(obj=step, request=bundle.request)
            step_data = step_resource.full_dehydrate(step_bundle)
            step_json = step_resource.serialize(None, step_data, 'application/json')
            step_dict = json.loads(step_json)
            step_class = step.load_step_class()
            step_dict['complete'] = step_class.is_complete(user=bundle.request.user)
            if step_dict['url']:
                serialized.append(step_dict)
        bundle.data['steps'] = serialized
        return bundle

    def alter_list_data_to_serialize(self, request, data):
        """
        Filter out any tours that are null. A tour will be returned as null if it is complete
        """
        data = super(TourResource, self).alter_list_data_to_serialize(request, data)
        data['objects'] = [obj for obj in data['objects'] if obj is not None]
        return data

    def apply_filters(self, request, applicable_filters):
        """
        Automatically filter the tour resource to return incomplete tours for a specific user
        """
        base_object_list = super(TourResource, self).apply_filters(request, applicable_filters)
        if request.GET.get('always_show'):
            base_object_list = base_object_list.filter(tourstatus__user=request.user)
        else:
            base_object_list = base_object_list.filter(tourstatus__user=request.user, tourstatus__complete=False)
        return base_object_list
