import datetime
from .models import Tour, Step, TourStatus


class BaseStep(object):
    """
    Base step class that handles the creation of step records and determines when the step is complete
    """
    def __init__(self, step):
        self.step = step

    def is_complete(self, user=None):
        """
        This is meant to be implemented in subclasses. This checks conditions to determine if the step is complete
        """
        return False

    def get_steps(self):
        """
        Returns the steps in order based on if there is a parent or not
        TODO: optimize this
        """
        all_steps = []
        steps = self.step.steps.all().filter(parent_step=self.step).order_by('sort_order')
        for step in steps:
            all_steps.append(step)
            all_steps.extend(step.load_step_class().get_steps())
        return all_steps


class BaseTour(object):
    """
    Base tour class that handles the creation of tour records and determines when tours are complete.
    """
    def __init__(self, tour):
        # self.current_step_class = None
        self.tour = tour

    def get_steps(self):
        """
        Returns the steps in order based on if there is a parent or not
        TODO: optimize this
        """
        all_steps = []
        steps = self.tour.steps.all().order_by('sort_order')
        for step in steps:
            all_steps.append(step)
            all_steps.extend(step.load_step_class().get_steps())
        return all_steps

    def get_url_list(self):
        """
        Returns a flattened list of urls of all steps contained in the tour.
        """
        return [step.url for step in self.tour.load_tour_class().get_steps() if step.url]

    def get_next_url(self):
        """
        Gets the next url based on the current step. The tour should always be fetched with
        Tour.objects.get_for_user so the is_complete method is called and the current step class
        gets set.
        """
        if self.current_step_class:
            return self.current_step_class.step.url
        return self.complete_url

    def add_user(self, user):
        """
        Adds a relationship record for the user
        """
        instance, created = TourStatus.objects.get_or_create(tour=self.tour, user=user, complete=False)
        return instance

    def is_complete(self, user=None):
        """
        Checks the state of the steps to see if they are all complete
        """
        self.current_step_class = None

        # Check the state of all steps
        for step in self.tour.get_steps():
            step_class = step.load_step_class()
            if self.current_step_class is None and step_class.is_complete(user=user) is False:
                self.current_step_class = step_class
        if self.current_step_class:
            return False
        self.mark_complete(user=user)
        return True

    def mark_complete(self, user=None):
        """
        Marks the tour record as complete and saves it.
        """
        if user:
            queryset = self.tour.tourstatus_set.all().filter(tour=self.tour, user=user, complete=False)
        else:
            queryset = self.tour.tourstatus_set.all().filter(tour=self.tour, complete=False)
        # Check if there are any incomplete records
        if queryset.count():
            complete_time = datetime.datetime.utcnow()
            queryset.update(complete=True, complete_time=complete_time)
            return True
        return False
