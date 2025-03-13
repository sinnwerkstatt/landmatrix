from .base import *

DATABASES["default"]["TEST"] = {
    "MIRROR": "default",  # Uses the existing database instead of creating a test one
}

DEBUG = False
SECRET_KEY = env("DJANGO_SECRET_KEY", default="MAGIC_CI_SECRET_KEY")

INTERNAL_IPS = ("127.0.0.1", "localhost")

TWITTER_TIMELINE = None
