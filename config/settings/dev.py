from .base import *

DEBUG = env.bool("DJANGO_DEBUG", default=True)
SECRET_KEY = env("DJANGO_SECRET_KEY", default="CHANGEME")
ALLOWED_HOSTS = ["*"]
INTERNAL_IPS = ("127.0.0.1",)


def is_package_installed(package_name):
    import importlib.util

    return importlib.util.find_spec(package_name) is not None


if is_package_installed("django_extensions"):
    # print("Adding 'django_extensions' to INSTALLED_APPS.")

    INSTALLED_APPS += ["django_extensions"]
else:
    print("django_extensions is not installed.")


# INSTALLED_APPS += ["wagtail.contrib.styleguide"]

SPECTACULAR_SETTINGS["PREPROCESSING_HOOKS"] = [
    "apps.api.spectacular.preprocess_exclude_wagtail",
]

HCAPTCHA_SITEKEY = "10000000-ffff-ffff-ffff-000000000001"
HCAPTCHA_SECRETKEY = "0x0000000000000000000000000000000000000000"
