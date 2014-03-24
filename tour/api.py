from tastypie.authentication import SessionAuthentication
from tastypie.authorization import Authorization
from tastypie.resources import ModelResource

from .models import Tour, Step


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
        queryset = Tour.objects.all().filter(tourstatus__complete=False)
        filtering = {
            'id': ['exact'],
        }

        authorization = Authorization()
        authentication = SessionAuthentication()

    def dehydrate_all(self, bundles, request):
        bundles = super(TourResource, self).dehydrate_all(bundles, request)

        # get child tours, check their status, and nest their data
        for bundle in bundles:
            bundle.obj.load_tour_class().is_complete()
            steps = bundle.obj.get_steps()
            serialized = []
            for step in steps:
                step_class = step.load_step_class()
                step_dict = {}
                # step_dict = get_api_model_dict(step, StepResource(), request)
                step_dict['complete'] = step_class.is_complete()
                if step_dict['url']:
                    serialized.append(step_dict)
            bundle.data['steps'] = serialized
        return bundles
