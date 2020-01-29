import os
import sys

import environ
from django.utils.translation import ugettext_lazy as _

BASE_DIR = environ.Path(__file__) - 3  # type: environ.Path

env = environ.Env()
env.read_env(BASE_DIR(".env"))

LANGUAGE_CODE = "en"
LANGUAGES = [("en", _("English")), ('de', _('German')), ("es", _("Español")), ("fr", _("Français"))]
TIME_ZONE = "Europe/Berlin"
USE_I18N = True
USE_L10N = True
USE_TZ = True
SITE_ID = 1

ROOT_URLCONF = "config.urls"
WSGI_APPLICATION = "config.wsgi.application"

EMAIL_CONFIG = env.email_url("DJANGO_EMAIL_URL", default="consolemail://")
vars().update(EMAIL_CONFIG)
SERVER_EMAIL = EMAIL_CONFIG["EMAIL_HOST_USER"]
DEFAULT_FROM_EMAIL = SERVER_EMAIL

DATABASES = {"default": env.db("DATABASE_URL")}

INSTALLED_APPS = [
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.humanize",
    "django.contrib.postgres",
    "wagtail_modeltranslation",
    "wagtail_modeltranslation.makemigrations",
    "wagtail_modeltranslation.migrate",
    "django.contrib.admin",
    "django.contrib.sites",
    # OL3 widgets must come before GIS
    "apps.ol3_widgets",
    "django.contrib.gis",
    # wagtail and dependencies
    "wagtail.contrib.forms",
    "wagtail.contrib.redirects",
    "wagtail.embeds",
    "wagtail.sites",
    "wagtail.users",
    "wagtail.snippets",
    "wagtail.documents",
    "wagtail.images",
    "wagtail.search",
    "wagtail.admin",
    "wagtail.core",
    "blog",
    "modelcluster",
    "taggit",
    "bootstrap3_datetime",
    # 'treebeard',
    "jstemplate",
    "simple_history",
    "crispy_forms",
    "wkhtmltopdf",
    "threadedcomments",
    "django_comments",
    "captcha",
    "rest_framework",
    "rest_framework.authtoken",
    "rest_framework_gis",
    "drf_yasg",
    "django.contrib.syndication",
    "file_resubmit",
    #   apps of the actual landmatrix project
    "apps.message",
    "apps.landmatrix",
    "apps.grid",
    "apps.map",
    "apps.charts",
    "apps.editor",
    "apps.wagtailcms",
    "apps.api",
    "apps.notifications",
    "apps.public_comments",
    "apps.feeds",
    "impersonate",
    "celery",
    "django_prometheus",
]

MIDDLEWARE = [
    "django_prometheus.middleware.PrometheusBeforeMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    # 'django.middleware.locale.LocaleMiddleware',
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    # populate the history user automatically
    "simple_history.middleware.HistoryRequestMiddleware",
    # wagtail and dependencies
    "wagtail.core.middleware.SiteMiddleware",
    "wagtail.contrib.redirects.middleware.RedirectMiddleware",
    "impersonate.middleware.ImpersonateMiddleware",
    "django_prometheus.middleware.PrometheusAfterMiddleware",
]

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR("templates")],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "django.contrib.auth.context_processors.auth",
                "django.template.context_processors.i18n",
                "django.template.context_processors.media",
                "django.template.context_processors.request",
                "django.contrib.messages.context_processors.messages",
                "apps.wagtailcms.context_processors.add_data_source_dir",
            ]
        },
    }
]

LOGIN_REDIRECT_URL = "/editor/"
# Limit all uploads to 20MB, and data sources to 1MB
MAX_UPLOAD_SIZE = 20971520
DATA_SOURCE_MAX_UPLOAD_SIZE = 10485760
DATA_SOURCE_DIR = "uploads"  # appended to MEDIA_ROOT/MEDIA_URL

MEDIA_ROOT = BASE_DIR("media")
MEDIA_URL = "/media/"
STATIC_ROOT = BASE_DIR("static-collected")
STATIC_URL = "/static/"
STATICFILES_FINDERS = [
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
    # 'compressor.finders.CompressorFinder',
]
STATICFILES_DIRS = [BASE_DIR("node_modules")]

FILE_UPLOAD_PERMISSIONS = 0o644

LOCALE_PATHS = [BASE_DIR("config/locale")]

CACHES = {
    "default": env.cache("DJANGO_CACHE_URL", default="dummycache://"),
    "file_resubmit": {
        "BACKEND": "django.core.cache.backends.filebased.FileBasedCache",
        "LOCATION": "/tmp/file_resubmit/",
    },
}

COMMENTS_APP = "apps.public_comments"

WAGTAIL_SITE_NAME = "Land Matrix"

MODELTRANSLATION_CUSTOM_FIELDS = ("NoWrapsStreamField",)

# Django REST Framework settings
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework.authentication.BasicAuthentication",
        "rest_framework.authentication.SessionAuthentication",
    )
}

IMPERSONATE = {
    "REDIRECT_URL": "/editor/",
    "REQUIRE_SUPERUSER": True,
    "ALLOW_SUPERUSER": True,
}

ELASTICSEARCH_URL = env("ELASTICSEARCH_URL", default="http://localhost")
try:
    ELASTIC_INDEX_AB = open(".es_index_ab_switch", "r").read()
except FileNotFoundError:
    open(".es_index_ab_switch", "w").write("a")
    ELASTIC_INDEX_AB = "a"
ELASTICSEARCH_INDEX_BASENAME = env("ELASTICSEARCH_INDEX_NAME", default="landmatrix")
ELASTICSEARCH_INDEX_NAME = f"{ELASTICSEARCH_INDEX_BASENAME}_{ELASTIC_INDEX_AB}"
print(f"Using elasticsearch index {ELASTICSEARCH_INDEX_NAME}")
sys.stdout.flush()

# CELERY SETTINGS
BROKER_URL = "redis://localhost:6379/0"
CELERY_REDIS_BACKEND = BROKER_URL
CELERY_NAME = "landmatrix"

BLOG_LIMIT_AUTHOR_CHOICES_GROUP = "CMS Global (Editors)"

# django-registration
ACCOUNT_ACTIVATION_DAYS = 7

WKHTMLTOPDF_CMD = env("DJANGO_WKHTMLTOPDF_CMD", default="wkhtmltopdf")

ALLOWED_HOSTS = env.list("DJANGO_ALLOWED_HOSTS", default=["127.0.0.1", "localhost"])

LANDMATRIX_INVESTOR_GRAPH_ENABLED = False
