from .base import *  # noqa

DEBUG = env.bool("DJANGO_DEBUG", default=True)
SECRET_KEY = env("DJANGO_SECRET_KEY", default="CHANGEME")

INTERNAL_IPS = ("127.0.0.1",)

RECAPTCHA_USE_SSL = True
NOCAPTCHA = True
RECAPTCHA_PUBLIC_KEY = "6LeIxAcTAAAAAJcZVRqyHh71UMIEGNQ_MXjiZKhI"
RECAPTCHA_PRIVATE_KEY = "6LeIxAcTAAAAAGG-vFI1TnRWxMZNFuojJ4WifJWe"
SILENCED_SYSTEM_CHECKS = ["captcha.recaptcha_test_key_error"]

BROKER_URL = "redis://redis:6379/0"
CELERY_REDIS_BACKEND = BROKER_URL
CELERY_NAME = "landmatrix"

ELASTICSEARCH_INDEX_NAMES = {
    "search_indexes.documents.deals": "test_deal",
    "search_indexes.documents.locations": "test_location",
}

CELERY_ENABLED = False
