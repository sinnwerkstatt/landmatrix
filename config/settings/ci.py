from .base import *  # noqa

DEBUG = env.bool('DJANGO_DEBUG', default=True)
SECRET_KEY = env("DJANGO_SECRET_KEY", default='CHANGEME')

INTERNAL_IPS = ('127.0.0.1',)

INSTALLED_APPS = [
                     'coverage',
                     'test_without_migrations',
                     'django_nose',
                     # 'debug_toolbar',
                     # 'template_timings_panel',
                 ] + INSTALLED_APPS

# Recaptcha spam protection for comments
# https://developers.google.com/recaptcha/docs/faq
RECAPTCHA_USE_SSL = True
NOCAPTCHA = True
RECAPTCHA_PUBLIC_KEY = "6LeIxAcTAAAAAJcZVRqyHh71UMIEGNQ_MXjiZKhI"
RECAPTCHA_PRIVATE_KEY = "6LeIxAcTAAAAAGG-vFI1TnRWxMZNFuojJ4WifJWe"
SILENCED_SYSTEM_CHECKS = ['captcha.recaptcha_test_key_error']

# Use nose to run all tests
TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'

# Tell nose to measure coverage on the 'foo' and 'bar' apps
# NOSE_ARGS = [
#    '--with-coverage',
#    '--cover-package=api,charts,editor,feeds,grid,landmatrix,map,wagtailcms'
# ]


ELASTICSEARCH_URL = 'http://elasticsearch'
BROKER_URL = 'redis://redis:6379/0'
CELERY_REDIS_BACKEND = BROKER_URL
CELERY_NAME = 'landmatrix'

CONVERT_DB = False
CONVERT_FROM_MY = False
TEST_AGAINST_LIVE_DB = False
