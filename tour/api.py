import json
from tastypie.authentication import SessionAuthentication
from tastypie.authorization import Authorization
from tastypie.resources import ModelResource

from .models import Tour, Step, TourStatus


class StepResource(ModelResource):

    class Meta:
        queryset = Step.objects.all()
        filtering = {
            'id': ['exact'],
        }

        authorization = Authorization()
        authentication = SessionAuthentication()


class TourResource(ModelResource):

    class Meta:
        queryset = Tour.objects.all()
        filtering = {
            'id': ['exact'],
        }

        authorization = Authorization()
        authentication = SessionAuthentication()

    def dehydrate(self, bundle):
        bundle = super(TourResource, self).dehydrate(bundle)
        is_complete = bundle.obj.load_tour_class().is_complete(user=bundle.request.user)
        if is_complete:
            return None
        steps = bundle.obj.get_steps()
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
        data = super(TourResource, self).alter_list_data_to_serialize(request, data)
        data['objects'] = [obj for obj in data['objects'] if obj is not None]
        return data

    def apply_filters(self, request, applicable_filters):
        base_object_list = super(TourResource, self).apply_filters(request, applicable_filters)
        base_object_list = base_object_list.filter(tourstatus__complete=False, tourstatus__user=request.user)
        return base_object_list
