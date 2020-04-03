import random
import string

from environ.environ import ImproperlyConfigured

from .base import *

DEBUG = False

WAGTAIL_ENABLE_UPDATE_CHECK = False

try:
    SECRET_KEY = env("DJANGO_SECRET_KEY")
except ImproperlyConfigured:
    SECRET_KEY = "".join(
        [
            random.SystemRandom().choice(
                "{}{}{}".format(string.ascii_letters, string.digits, "+-:$;<=>?@^_~")
            )
            for i in range(63)
        ]
    )
    with open(".env", "a") as envfile:
        envfile.write("DJANGO_SECRET_KEY={}\n".format(SECRET_KEY))

INSTALLED_APPS += ["raven.contrib.django.raven_compat"]

RAVEN_CONFIG = {
    "dsn": env("DJANGO_RAVEN_DSN"),
    "string_max_length": 12000,
    "list_max_length": 1200,
}

CELERY_TASK_ALWAYS_EAGER = True

# Recaptcha spam protection for comments
# https://developers.google.com/recaptcha/docs/faq
RECAPTCHA_USE_SSL = True
NOCAPTCHA = True
RECAPTCHA_PUBLIC_KEY = env("DJANGO_RECAPTCHA_PUBLIC_KEY")
RECAPTCHA_PRIVATE_KEY = env("DJANGO_RECAPTCHA_PRIVATE_KEY")
