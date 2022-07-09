import random
import string

import sentry_sdk

# noinspection PyPackageRequirements
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
                f"{string.ascii_letters}{string.digits}{'+-:$;<=>?@^_~'}"
            )
            for i in range(63)
        ]
    )
    with open(".env", "a", encoding="UTF-8") as envfile:
        envfile.write(f"DJANGO_SECRET_KEY={SECRET_KEY}\n")

sentry_sdk.init(
    dsn=env("DJANGO_SENTRY_DSN"),
    integrations=[DjangoIntegration()],
    send_default_pii=True,
)

CELERY_TASK_ALWAYS_EAGER = True

HCAPTCHA_SITEKEY = env("DJANGO_HCAPTCHA_SITEKEY")
HCAPTCHA_SECRETKEY = env("DJANGO_HCAPTCHA_SECRETKEY")
