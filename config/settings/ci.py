from .base import *  # noqa

DEBUG = True
SECRET_KEY = "MAGIC_CI_SECRET_KEY"

INTERNAL_IPS = ("127.0.0.1",)

TWITTER_TIMELINE = None


BROKER_URL = "redis://redis:6379/0"
CELERY_REDIS_BACKEND = BROKER_URL
CELERY_NAME = "landmatrix"
