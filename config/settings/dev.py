from .base import *  # noqa

DEBUG = env.bool("DJANGO_DEBUG", default=True)
SECRET_KEY = env("DJANGO_SECRET_KEY", default="CHANGEME")

INTERNAL_IPS = ("127.0.0.1",)

try:
    import django_extensions

    INSTALLED_APPS += ["django_extensions"]
except ModuleNotFoundError:
    pass

try:
    import debug_toolbar

    INSTALLED_APPS += ["debug_toolbar"]
    MIDDLEWARE += ["debug_toolbar.middleware.DebugToolbarMiddleware"]

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
