from .base import *  # noqa

DEBUG = env.bool("DJANGO_DEBUG", default=True)
SECRET_KEY = env("DJANGO_SECRET_KEY", default="CHANGEME")
ALLOWED_HOSTS = ["*"]
INTERNAL_IPS = ("127.0.0.1",)

try:
    import django_extensions  # type: ignore

    INSTALLED_APPS += ["django_extensions"]
except ModuleNotFoundError:
    print("not using django_extensions...")
    pass


# INSTALLED_APPS += ["wagtail.contrib.styleguide"]

SPECTACULAR_SETTINGS["PREPROCESSING_HOOKS"] = [
    "apps.api.spectacular.preprocess_exclude_wagtail",
]

HCAPTCHA_SITEKEY = "10000000-ffff-ffff-ffff-000000000001"
HCAPTCHA_SECRETKEY = "0x0000000000000000000000000000000000000000"
