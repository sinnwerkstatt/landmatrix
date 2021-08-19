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

# Recaptcha spam protection for comments
# https://developers.google.com/recaptcha/docs/faq
RECAPTCHA_USE_SSL = True
NOCAPTCHA = True
RECAPTCHA_PUBLIC_KEY = "6LeIxAcTAAAAAJcZVRqyHh71UMIEGNQ_MXjiZKhI"
RECAPTCHA_PRIVATE_KEY = "6LeIxAcTAAAAAGG-vFI1TnRWxMZNFuojJ4WifJWe"
SILENCED_SYSTEM_CHECKS = ["captcha.recaptcha_test_key_error"]
LANDMATRIX_INVESTOR_GRAPH_ENABLED = True

# hCaptcha spam protection for comments
HCAPTCHA_SITEKEY = "10000000-ffff-ffff-ffff-000000000001"
HCAPTCHA_SECRETKEY = "0x0000000000000000000000000000000000000000"


# CACHES["default"] = {
#     "BACKEND": "django.core.cache.backends.memcached.MemcachedCache",
#     "LOCATION": "127.0.0.1:11211",
# }
# /etc/memcached.conf -> `-I 128M`
