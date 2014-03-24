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
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Framework :: Django',
    ],
    license='MIT',
    install_requires=[
        'django>=1.6',
    ],
    tests_require=[
        'psycopg2',
        'django-nose',
        'south',
    ],
    test_suite='run_tests.run_tests',
    include_package_data=True,
)
