"""
Simplest possible settings.py for use in running django_highrise unit tests.

This settings file would be completely useless for running a project, however
it has enough in it to be able to run the django unit test runner, and to spin
up django.contrib.auth users (as required by django_highrise).

In order for the tests to run, you will need to set the following environment
variables: HIGHRISE_SERVER and HIGHRISE_API_KEY.

Please see online documentation for more details.
"""
from os import environ as env
from sys import exit
import logging

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'delme'
    }
}

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django_highrise'
)

# this isn't used, however the django_highrise app does reference a logger,
# so although the tests will run without this, some warnings will appear.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
    },
    'loggers': {
        '': {
            'handlers': ['console'],
            'propagate': False,
            'level': 'DEBUG',
        },
    }
}

try:
    HIGHRISE_SERVER = env['HIGHRISE_SERVER']
    HIGHRISE_API_KEY = env['HIGHRISE_API_KEY']
except KeyError:
    logging.error("Missing environment variables HIGHRISE_SERVER and "
        "HIGHRISE_API_KEY. Please set these before attempting to run tests.")
    exit(1)
