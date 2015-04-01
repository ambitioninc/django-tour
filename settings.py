import os

import django
from django.conf import settings


def configure_settings():
    if not settings.configured:
        # Determine the database settings depending on if a test_db var is set in CI mode or not
        test_db = os.environ.get('DB', None)
        if test_db is None:
            db_config = {
                'ENGINE': 'django.db.backends.postgresql_psycopg2',
                'NAME': 'ambition_dev',
                'USER': 'ambition_dev',
                'PASSWORD': 'ambition_dev',
                'HOST': 'localhost'
            }
        elif test_db == 'postgres':
            db_config = {
                'ENGINE': 'django.db.backends.postgresql_psycopg2',
                'USER': 'postgres',
                'NAME': 'tour',
            }
        else:
            raise RuntimeError('Unsupported test DB {0}'.format(test_db))

        settings.configure(
            MIDDLEWARE_CLASSES=(),
            DATABASES={
                'default': db_config,
            },
            INSTALLED_APPS=(
                'django.contrib.auth',
                'django.contrib.contenttypes',
                'django.contrib.sessions',
                'django.contrib.admin',
                'tour',
                'tour.tests',
            ) + (('south',) if django.VERSION[1] <= 6 else ()),
            ROOT_URLCONF='tour.urls',
            DEBUG=False,
        )
