from django.conf import settings
from django.db import models
from django.utils.module_loading import import_by_path
from manager_utils import ManagerUtilsManager
import six


class TourManager(ManagerUtilsManager):
    """
    Provides extra functionality for the Tour model
    """
    def complete_tours(self, user):
        """
        Marks any completed tours as complete
        """
        if not user.pk:
            return None
        tours = self.filter(tourstatus__user=user, tourstatus__complete=False)
        for tour in tours:
            tour_class = tour.load_tour_class()
            if tour_class.is_complete(user):
                tour_class.mark_complete(user)

    def get_for_user(self, user):
        """
        Checks if a tour exists for a user and returns the tour instance
        """
        if not user.pk:
            return None
        self.complete_tours(user)
        return self.filter(tourstatus__user=user, tourstatus__complete=False).first()

    def get_recent_tour(self, user):
        if not user.pk:
            return None
        return self.filter(tourstatus__user=user).order_by(
            'tourstatus__complete', '-tourstatus__complete_time').first()

    def get_next_url(self, user):
        """
        Convenience method to get the next url for the specified user
        """
        if not user.pk:
            return None
        tour = self.get_for_user(user)
        if not tour:
            tour = self.get_recent_tour(user)
        if tour:
            return tour.load_tour_class().get_next_url(user)
        return None


@six.python_2_unicode_compatible
class Tour(models.Model):
    """
    Container object for tour steps. Provides functionality for loading the tour logic class
    and fetching the steps in the correct order.
    """
    name = models.CharField(max_length=128, unique=True)
    display_name = models.CharField(max_length=128)
    tour_class = models.CharField(max_length=128, unique=True)
    users = models.ManyToManyField(settings.AUTH_USER_MODEL, through='TourStatus')
    complete_url = models.CharField(max_length=128, blank=True, null=True, default=None)

    objects = TourManager()

    def load_tour_class(self):
        """
        Imports and returns the tour class.
        :return: The tour class instance determined by `tour_class`
        :rtype: BaseTour
        """
        return import_by_path(self.tour_class)(self)

    def __str__(self):
        return '{0}'.format(self.display_name)


@six.python_2_unicode_compatible
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

    objects = ManagerUtilsManager()

    def load_step_class(self):
        """
        Imports and returns the step class.
        """
        return import_by_path(self.step_class)(self)

    def __str__(self):
        return '{0}'.format(self.display_name)


class TourStatus(models.Model):
    """
    This is the model that represents the relationship between a user and a tour. Keeps
    track of whether the tour has been completed by a user.
    """
    tour = models.ForeignKey(Tour)
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    complete = models.BooleanField(default=False)
    create_time = models.DateTimeField(auto_now_add=True)
    complete_time = models.DateTimeField(null=True, blank=True, default=None)

    objects = ManagerUtilsManager()
