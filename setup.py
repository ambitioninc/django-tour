# import multiprocessing to avoid this bug (http://bugs.python.org/issue15881#msg170215)
import multiprocessing
assert multiprocessing
import re
from setuptools import setup, find_packages


def get_version():
    """
    Extracts the version number from the version.py file.
    """
    VERSION_FILE = 'tour/version.py'
    mo = re.search(r'^__version__ = [\'"]([^\'"]*)[\'"]', open(VERSION_FILE, 'rt').read(), re.M)
    if mo:
        return mo.group(1)
    else:
        raise RuntimeError('Unable to find version string in {0}.'.format(VERSION_FILE))


setup(
    name='django-tour',
    version=get_version(),
    description='Require the django user to complete a series of steps with custom logic',
    long_description=open('README.md').read(),
    url='https://github.com/ambitioninc/django-tour',
    author='Wes Okes',
    author_email='wes.okes@gmail.com',
    keywords='',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Framework :: Django',
        'Framework :: Django :: 1.6',
        'Framework :: Django :: 1.7',
    ],
    license='MIT',
    install_requires=[
        'Django>=1.6',
        'djangorestframework>=2.3.13,<3.0',
        'django-manager-utils>=0.7.2',
        'django_filter>=0.7',
    ],
    tests_require=[
        'psycopg2',
        'django-nose',
        'mock',
        'south>=1.0.2',
        'django_dynamic_fixture',
    ],
    test_suite='run_tests.run_tests',
    include_package_data=True,
)
