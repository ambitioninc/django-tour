from rest_framework import serializers
from tour.models import Tour, Step


class TourSerializer(serializers.ModelSerializer):
    steps = serializers.SerializerMethodField('get_steps')

    class Meta:
        model = Tour
        fields = ('name', 'display_name', 'complete_url', 'steps')

    def get_steps(self, tour):
        return [StepSerializer(child_step).data for child_step in tour.load_tour_class().get_steps(0)]


class StepSerializer(serializers.ModelSerializer):
    steps = serializers.SerializerMethodField('get_steps')

    class Meta:
        model = Step
        fields = ('name', 'display_name', 'url', 'sort_order', 'steps')

    def get_steps(self, step):
        return [StepSerializer(child_step).data for child_step in step.load_step_class().get_steps(0)]
