
from .base import *  # noqa

DEBUG = env.bool('DJANGO_DEBUG', default=True)
SECRET_KEY = env("DJANGO_SECRET_KEY", default='CHANGEME')

INTERNAL_IPS = ('127.0.0.1',)


# try:
#     import django_extensions
#     INSTALLED_APPS += ['django_extensions']
# except ModuleNotFoundError:
#     pass

# try:
#     import debug_toolbar
#     INSTALLED_APPS += ['debug_toolbar']
#     MIDDLEWARE += ['debug_toolbar.middleware.DebugToolbarMiddleware']
#
# except ModuleNotFoundError:
#     pass


INSTALLED_APPS = [
    'coverage',
    'test_without_migrations',
    'django_nose',
    # 'debug_toolbar',
    # 'template_timings_panel',
    ] + INSTALLED_APPS


if env.bool('FRONTENDDEV', default=False):
    INSTALLED_APPS = [
        'django_gulp',
        'livereload'
    ] + INSTALLED_APPS

    MIDDLEWARE += ['livereload.middleware.LiveReloadScript']


DEBUG_TOOLBAR_PANELS = [
    'debug_toolbar.panels.versions.VersionsPanel',
    'debug_toolbar.panels.timer.TimerPanel',
    'debug_toolbar.panels.settings.SettingsPanel',
    'debug_toolbar.panels.headers.HeadersPanel',
    'debug_toolbar.panels.request.RequestPanel',
    'debug_toolbar.panels.sql.SQLPanel',
    'debug_toolbar.panels.staticfiles.StaticFilesPanel',
    'debug_toolbar.panels.templates.TemplatesPanel',
    'debug_toolbar.panels.cache.CachePanel',
    'debug_toolbar.panels.signals.SignalsPanel',
    'debug_toolbar.panels.logging.LoggingPanel',
    'debug_toolbar.panels.redirects.RedirectsPanel',
    'template_timings_panel.panels.TemplateTimings.TemplateTimings',
]

# Recaptcha spam protection for comments
# https://developers.google.com/recaptcha/docs/faq
RECAPTCHA_USE_SSL = True
NOCAPTCHA = True
RECAPTCHA_PUBLIC_KEY = "6LeIxAcTAAAAAJcZVRqyHh71UMIEGNQ_MXjiZKhI"
RECAPTCHA_PRIVATE_KEY = "6LeIxAcTAAAAAGG-vFI1TnRWxMZNFuojJ4WifJWe"
SILENCED_SYSTEM_CHECKS = ['captcha.recaptcha_test_key_error']


# Use nose to run all tests
TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'

# Tell nose to measure coverage on the 'foo' and 'bar' apps
#NOSE_ARGS = [
#    '--with-coverage',
#    '--cover-package=api,charts,editor,feeds,grid,landmatrix,map,wagtailcms'
#]

