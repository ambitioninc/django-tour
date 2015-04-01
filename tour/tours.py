import datetime

from tour.models import TourStatus


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
        return True

    def get_steps(self, depth=-1):
        """
        Returns the steps in order based on if there is a parent or not
        TODO: optimize this
        """
        all_steps = []
        steps = self.step.steps.filter(parent_step=self.step).order_by('sort_order')
        for step in steps:
            all_steps.append(step)
            if depth != 0:
                all_steps.extend(step.load_step_class().get_steps(depth=depth - 1))
        return all_steps


class BaseTour(object):
    """
    Base tour class that handles the creation of tour records and determines when tours are complete.
    """
    def __init__(self, tour):
        # self.current_step_class = None
        self.tour = tour

    def get_steps(self, depth=-1):
        """
        Returns the steps in order based on if there is a parent or not
        TODO: optimize this
        """
        all_steps = []
        steps = self.tour.steps.filter(parent_step=None).order_by('sort_order')
        for step in steps:
            all_steps.append(step)
            if depth != 0:
                all_steps.extend(step.load_step_class().get_steps(depth=depth - 1))
        return all_steps

    def get_url_list(self):
        """
        Returns a flattened list of urls of all steps contained in the tour.
        """
        return [step.url for step in self.get_steps() if step.url]

    def add_user(self, user):
        """
        Adds a relationship record for the user
        """
        instance, created = TourStatus.objects.get_or_create(tour=self.tour, user=user, complete=False)
        return instance

    def mark_complete(self, user):
        """
        Marks the tour status record as complete
        """
        tour_status = self.tour.tourstatus_set.all().filter(tour=self.tour, user=user, complete=False).first()
        if tour_status:
            tour_status.complete = True
            tour_status.complete_time = datetime.datetime.utcnow()
            tour_status.save()
            return True
        return False

    def get_current_step(self, user):
        """
        Finds the first incomplete steps and returns it
        :param user: The django user to find the current step for
        :type user: User
        :return: The first incomplete step
        :rtype: Step
        """
        for step in self.get_steps():
            if not step.load_step_class().is_complete(user):
                return step
        return None

    def get_next_url(self, user):
        """
        Gets the next url based on the current step.
        """
        current_step = self.get_current_step(user)
        return current_step.url if current_step else self.tour.complete_url

    def is_complete(self, user):
        """
        Checks the state of the steps to see if they are all complete
        """
        return False if self.get_current_step(user) else True
