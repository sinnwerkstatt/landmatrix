import random
import string

import sentry_sdk
from environ.environ import ImproperlyConfigured
from sentry_sdk.integrations.django import DjangoIntegration

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

sentry_sdk.init(
    dsn=env("DJANGO_SENTRY_DSN"),
    integrations=[DjangoIntegration()],
    send_default_pii=True,
)

CELERY_TASK_ALWAYS_EAGER = True

# Recaptcha spam protection for comments
# https://developers.google.com/recaptcha/docs/faq
RECAPTCHA_USE_SSL = True
NOCAPTCHA = True
RECAPTCHA_PUBLIC_KEY = env("DJANGO_RECAPTCHA_PUBLIC_KEY")
RECAPTCHA_PRIVATE_KEY = env("DJANGO_RECAPTCHA_PRIVATE_KEY")

HCAPTCHA_SITEKEY = env("DJANGO_HCAPTCHA_SITEKEY")
HCAPTCHA_SECRETKEY = env("DJANGO_HCAPTCHA_SECRETKEY")
