[![Build Status](https://travis-ci.org/ambitioninc/django-tour.png)](https://travis-ci.org/ambitioninc/django-tour)
## Django Tour

Django Tour is a `django>=1.6` app that helps navigate a user through a series of pages and ensures that
each step is successfully completed. A template tag is available to show the user the current progress
through the tour by showing a simple UI. This UI can be styled and modified to suit different display scenarios.
A single tour can be assigned to any number of users, and the completion of the steps can be per user or shared.

## Table of Contents

1. [Installation] (#installation)
1. [Creating a Tour] (#creating-a-tour)
1. [Displaying the Navigation] (#displaying-the-navigation)
1. [Changes](#changes)

## Installation
To install Django Tour:

```shell
pip install git+https://github.com/ambitioninc/django-tour.git
```

Add Django Tour to your `INSTALLED_APPS` to get started:

settings.py

```python
# Simply add 'tour' to your installed apps.
# Django Tour relies on several basic django apps.
INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.admin',
    'django.contrib.sites',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.contenttypes',
    'tour',
)
```

Make sure Django's CsrfViewMiddleware is enabled:

settings.py

```python
MIDDLEWARE_CLASSES = (
    'django.middleware.csrf.CsrfViewMiddleware',
)
```

Add Django Tour's urls to your project:

urls.py

```python
from django.conf.urls import include, patterns, url

urlpatterns = patterns(
    url(r'^tour/', include('tour.urls')),
)
```

## Creating a Tour

Any app that wants to define a tour should first create a tours.py file. This is where all of the custom
logic will be contained. Start off by defining the steps needed for the tour; these steps should inherit from
`BaseStep`.

##### `step_class`
The full python path to the class

##### `name`
The display name that will be used for this step of the tour.


```python
from tour.tours import BaseStep, BaseTour


class FirstStep(BaseStep):
    step_class = 'path.to.FirstStep'
    name = 'First Step'

    @classmethod
    def get_url(cls):
        return reverse('example.first_step')

    def is_complete(self, user=None):
        return some_method(user)


class SecondStep(BaseStep):
    step_class = 'path.to.SecondStep'
    name = 'Second Step'

    @classmethod
    def get_url(cls):
        return reverse('example.second_step')

    def is_complete(self, user=None):
        return some_other_method(user)
```

Next, set up the tour class to contain these steps. The tour should inherit from `BaseTour` and a few attributes
need to be set.

##### `tour_class`
The python path to the tour class

##### `name`
The display name that will be used in the tour UI

##### `steps`
A list of step classes in the order they need to be completed

##### `complete_url`
The url that will be returned when calling `get_next_url` after the tour is considered complete

```python
class ExampleTour(BaseTour):
    tour_class = 'path.to.ExampleTour'
    name = 'Example Tour'
    complete_url = '/page/finished/'
    steps = [
        FirstStep,
        SecondStep,
    ]
```

It is up to your application code to determine when a user should be assigned a tour.

```python
from django.contrib.auth.models import User

from path.to import ExampleTour


user = User.objects.get(id=1)
ExampleTour.add_user(user)
```

This will create a `TourStatus` instance linking `user` to the `ExampleTour` with `complete` set to False. The
`add_user` method will automatically call `ExampleTour.create()` if there isn't already a tour record. The
`create` method takes care of making records for each of the steps as well.

## Displaying the Navigation

In your django template all you need to do is load the tour tags with `{% load tour_tags %}` then put the
`{% tour_navigation %}` tag where it should appear. When the user loads the template, a check will be performed
to see if the user has any incomplete tours. If there is a tour, the navigation will be displayed.

If it makes sense to always display the tour navigation even after the final step is complete, then pass the
always_show argument to the tour tag `{% tour_navigation always_show=True %}`

## Restricting View Access

If the order of step completion is important for a tour, the view mixin `TourStepMixin` can be added to any
django view that is part of the tour. The step is identified by the url of the view and if the user
tries to access a page out of order, they will be redirected to the first incomplete step of the tour.
Once a tour has been completed, the user will also be prevented from visiting other steps that inherit
form the `TourStepMixin` in the tour.

```python
class MyView(TourStepMixin, TemplateView):
    """ view config """
```

# Changes

-  0.6.3
  - Updated to `Tour` and `TourStatus` models Foreign Key to `settings.AUTH_USER_MODEL`
- 0.6.2
  - Added Django 1.7 support
