from django.contrib.auth.models import User
from django.db import models

from tour.utils.import_string import import_string


class TourManager(models.Manager):
    """
    Provides extra functionality for the Tour model
    """
    def get_for_user(self, user):
        """
        Checks if a tour exists for a user and returns the instantiated tour object
        """
        if not user.pk:
            return None
        queryset = self
        tours = queryset.filter(tourstatus__user=user, tourstatus__complete=False).order_by('-tourstatus__create_time')
        for tour in tours:
            tour_class = tour.load_tour_class()
            if tour_class.is_complete(user=user) is False:
                return tour_class
        return None

    def get_recent_tour(self, user):
        if not user.pk:
            return None
        tour = self.filter(tourstatus__user=user).order_by(
            'tourstatus__complete', '-tourstatus__complete_time').first()
        if tour:
            return tour.load_tour_class()
        return None

    def get_next_url(self, user):
        """
        Convenience method to get the next url for the specified user
        """
        tour_class = self.get_for_user(user)
        if not tour_class:
            tour_class = self.get_recent_tour(user)
        if tour_class:
            return tour_class.get_next_url()
        return None


class Tour(models.Model):
    """
    Container object for tour steps. Provides functionality for loading the tour logic class
    and fetching the steps in the correct order.
    """
    name = models.CharField(max_length=128, unique=True)
    display_name = models.CharField(max_length=128)
    tour_class = models.CharField(max_length=128, unique=True)
    users = models.ManyToManyField(User, through='TourStatus')
    complete_url = models.CharField(max_length=128, blank=True, null=True, default=None)

    objects = TourManager()

    def load_tour_class(self):
        """
        Imports and returns the tour class.
        """
        return import_string(self.tour_class)(self)

    def __unicode__(self):
        return u'{0}'.format(self.display_name)


class Step(models.Model):
    """
    Represents one step of the tour that must be completed. The custom logic is implemented
    in the class specified in step_class
    """
    name = models.CharField(max_length=128, unique=True)
    display_name = models.CharField(max_length=128)
    url = models.CharField(max_length=128, null=True, blank=True)
    tour = models.ForeignKey(Tour, related_name='steps')
    parent_step = models.ForeignKey('self', null=True, related_name='steps')
    step_class = models.CharField(max_length=128, unique=True)
    sort_order = models.IntegerField(default=0)

    def load_step_class(self):
        """
        Imports and returns the step class.
        """
        return import_string(self.step_class)(self)

    def __unicode__(self):
        return u'{0}'.format(self.display_name)


class TourStatus(models.Model):
    """
    This is the model that represents the relationship between a user and a tour. Keeps
    track of whether the tour has been completed by a user.
    """
    tour = models.ForeignKey(Tour)
    user = models.ForeignKey(User)
    complete = models.BooleanField(default=False)
    create_time = models.DateTimeField(auto_now_add=True)
    complete_time = models.DateTimeField(null=True, blank=True, default=None)
