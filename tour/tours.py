from .models import Tour, Step, TourStatus
from tour.exceptions import MissingStepClass, MissingTourClass


class BaseStep(object):
    """
    Base step class that handles the creation of step records and determines when the step is complete
    """
    step_class = None
    name = None
    parent_step = None

    def __init__(self, step):
        self.step = step

    @classmethod
    def get_url(cls):
        return None

    @classmethod
    def create(cls, tour):
        """
        Creates the step record
        """
        if cls.step_class is None:
            raise MissingStepClass('Step {0} needs a step_class in order to call create'.format(cls))

        # Get parent step if needed
        parent_step = None
        if cls.parent_step:
            parent_step = Step.objects.get(step_class=cls.parent_step.step_class)

        instance, created = Step.objects.get_or_create(
            step_class=cls.step_class, tour=tour, defaults=dict(
                name=cls.name,
                url=cls.get_url(),
                parent_step=parent_step,
            )
        )

        return instance

    def is_complete(self, user=None):
        """
        This is meant to be implemented in subclasses. This checks conditions to determine if the step is complete
        """
        return False


class BaseTour(object):
    """
    Base tour class that handles the creation of tour records and determines when tours are complete.
    """
    tour_class = None
    name = None
    steps = []
    parent_tour = None

    def __init__(self, tour):
        self.current_step_class = None
        self.tour = tour

    @classmethod
    def create(cls):
        """
        Creates the tour record
        """
        if cls.tour_class is None:
            raise MissingTourClass('Tour {0} needs a tour_class in order to call create'.format(cls))

        tour_class = cls.tour_class
        if cls.parent_tour:
            tour_class = cls.parent_tour.tour_class

        instance, created = Tour.objects.get_or_create(
            tour_class=tour_class, defaults=dict(
                name=cls.name
            )
        )

        # Make sure steps exist
        for step in cls.steps:
            step.create(instance)

        return instance

    @classmethod
    def delete(cls):
        Tour.objects.filter(tour_class=cls.tour_class).delete()

    @classmethod
    def add_user(cls, user):
        try:
            tour = Tour.objects.get(tour_class=cls.tour_class)
        except Exception:
            tour = cls.create()

        instance, created = TourStatus.objects.get_or_create(tour=tour, user=user, complete=False)
        return instance

    def get_next_url(self):
        """
        Gets the next url based on the current step. The tour should always be fetched with
        Tour.objects.get_for_user so the is_complete method is called and the current step class
        gets set.
        """
        if self.current_step_class:
            return self.current_step_class.step.url
        return None

    def get_url_list(self):
        return [step.url for step in self.tour.get_steps() if step.url]

    def is_complete(self, user=None):
        """
        Checks the state of the steps to see if they are all complete
        """
        # Check the state of all steps
        for step in self.tour.get_steps():
            step_class = step.load_step_class()
            if step_class.is_complete(user=user) is False:
                self.current_step_class = step_class
                return False
        self.mark_complete(user=user)
        return True

    def mark_complete(self, user=None):
        """
        Marks the tour record as complete and saves it.
        """
        if user:
            self.tour.tourstatus_set.all().filter(tour=self.tour, user=user).update(complete=True)
        else:
            self.tour.tourstatus_set.all().filter(tour=self.tour).update(complete=True)
