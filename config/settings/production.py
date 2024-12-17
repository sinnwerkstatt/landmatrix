import random
import string

import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

from .base import *  # noqa

DEBUG = False

WAGTAIL_ENABLE_UPDATE_CHECK = False

try:
    SECRET_KEY = env("DJANGO_SECRET_KEY")
except environ.ImproperlyConfigured:
    SECRET_KEY = "".join(
        [
            random.SystemRandom().choice(
                f"{string.ascii_letters}{string.digits}{'+-:$;<=>?@^_~'}"
            )
            for i in range(63)
        ]
    )
    with open(ENV_PATH, "a", encoding="UTF-8") as envfile:
        envfile.write(f"\nDJANGO_SECRET_KEY={SECRET_KEY}\n")

sentry_sdk.init(
    dsn=env("DJANGO_SENTRY_DSN"),
    integrations=[DjangoIntegration()],
    send_default_pii=True,
)

HCAPTCHA_SITEKEY = env("DJANGO_HCAPTCHA_SITEKEY")
HCAPTCHA_SECRETKEY = env("DJANGO_HCAPTCHA_SECRETKEY")
