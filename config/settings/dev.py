from .base import *  # noqa

DEBUG = env.bool("DJANGO_DEBUG", default=True)
SECRET_KEY = env("DJANGO_SECRET_KEY", default="CHANGEME")

INTERNAL_IPS = ("127.0.0.1",)

try:
    import django_extensions

    INSTALLED_APPS += ["django_extensions"]
except ModuleNotFoundError:
    pass


if env.bool("FRONTENDDEV", default=False):
    INSTALLED_APPS = [
        # 'django_gulp',
        "livereload"
    ] + INSTALLED_APPS

    MIDDLEWARE += ["livereload.middleware.LiveReloadScript"]

SPECTACULAR_SETTINGS["PREPROCESSING_HOOKS"] = []

# hCaptcha spam protection for comments
HCAPTCHA_SITEKEY = "10000000-ffff-ffff-ffff-000000000001"
HCAPTCHA_SECRETKEY = "0x0000000000000000000000000000000000000000"
