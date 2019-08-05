import random
import string
from environ.environ import ImproperlyConfigured

from .base import *  # noqa


# Recaptcha spam protection for comments
# https://developers.google.com/recaptcha/docs/faq
RECAPTCHA_USE_SSL = True
NOCAPTCHA = True
RECAPTCHA_PUBLIC_KEY = env("DJANGO_RECAPTCHA_PUBLIC_KEY")
RECAPTCHA_PRIVATE_KEY = env("DJANGO_RECAPTCHA_PRIVATE_KEY")


TWITTER_TIMELINE = {
    'consumer_key': 'lDSsFwPuVqIvWNTVqYrkPgqVx',
    'consumer_secret': 'zUXtLPCCyV6E1uskfNAOUDqLSeqeNY5ZQDtIHxaq1ZNCdj1YEv',
    'access_token': '182320767-qDBHP42oBPyiLFPtP1IDQHiGhFLUu5eTofcTLfRW',
    'access_token_secret': '5VJCSXUmuenivcm6Z1r23Na1TOwnQkRbcNws9LBg13nN7'
}




# whether to show SQL generated (is referenced below when configuring logging)

DEBUG = False

# INSTALLED_APPS = (
#     'coverage',
#     'test_without_migrations',
#     'django_nose',
# ) + INSTALLED_APPS


# LOGGING = {
#     'version': 1,
#     'disable_existing_loggers': True,
#     'formatters': {
#         'simple': {
#             'format': '%(levelname)s %(message)s',
#              'datefmt': '%y %b %d, %H:%M:%S',
#             },
#         },
#     'handlers': {
#         'console': {
#             'level': 'DEBUG',
#             'class': 'logging.StreamHandler',
#             'formatter': 'simple'
#         },
#         'celery': {
#             'level': 'DEBUG',
#             'class': 'logging.handlers.RotatingFileHandler',
#             'filename': 'celery.log',
#             'formatter': 'simple',
#             'maxBytes': 1024 * 1024 * 100,  # 100 mb
#         },
#     },
#     'loggers': {
#         'celery': {
#             'handlers': ['celery', 'console'],
#             'level': 'DEBUG',
#         },
#     }
# }

#CACHES = {
#   'default': {
#       'BACKEND': 'django.core.cache.backends.memcached.PyLibMCCache',
#       'LOCATION': '127.0.0.1:11211',
#   }
#}

CELERY_TASK_ALWAYS_EAGER = True

try:
    SECRET_KEY = env("DJANGO_SECRET_KEY")
except ImproperlyConfigured:
    SECRET_KEY = ''.join(
        [random.SystemRandom().choice("{}{}{}".format(string.ascii_letters, string.digits, '+-:$;<=>?@^_~')) for i in
         range(63)])
    with open('.env', 'a') as envfile:
        envfile.write('DJANGO_SECRET_KEY={}\n'.format(SECRET_KEY))
