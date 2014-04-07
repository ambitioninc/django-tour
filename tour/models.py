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
        queryset = self
        tours = queryset.filter(tourstatus__user=user, tourstatus__complete=False)
        for tour in tours:
            tour_class = tour.load_tour_class()
            if tour_class.is_complete(user=user) is False:
                return tour_class
        return None

    def get_next_url(self, user):
        """
        Convenience method to get the next url for the specified user
        """
        tour = self.get_for_user(user)
        if not tour:
            return None
        return tour.get_next_url()


class Tour(models.Model):
    """
    Container object for tour steps. Provides functionality for loading the tour logic class
    and fetching the steps in the correct order.
    """
    name = models.CharField(max_length=128, unique=True)
    tour_class = models.CharField(max_length=128, unique=True)
    users = models.ManyToManyField(User, through='TourStatus')

    objects = TourManager()

    # TODO: look into callable field app
    def load_tour_class(self):
        """
        Imports and returns the tour class.
        """
        return import_string(self.tour_class)(self)

    def get_steps(self, parent_step=None):
        """
        Returns the steps in order based on if there is a parent or not
        TODO: optimize this
        """
        all_steps = []
        steps = self.step_set.all().filter(parent_step=parent_step).order_by('id')
        for step in steps:
            all_steps.append(step)
            all_steps += self.get_steps(step)
        return all_steps


class Step(models.Model):
    """
    Represents one step of the tour that must be completed. The custom logic is implemented
    in the class specified in step_class
    """
    name = models.CharField(max_length=128, unique=True)
    url = models.CharField(max_length=128, null=True, blank=True)
    tour = models.ForeignKey(Tour)
    parent_step = models.ForeignKey('self', null=True, related_name='child_steps')
    step_class = models.CharField(max_length=128, unique=True)

    def load_step_class(self):
        """
        Imports and returns the step class.
        """
        return import_string(self.step_class)(self)


class TourStatus(models.Model):
    """
    This is the model that represents the relationship between a user and a tour. Keeps
    track of whether the tour has been completed by a user.
    """
    tour = models.ForeignKey(Tour)
    user = models.ForeignKey(User)
    complete = models.BooleanField(default=False)
