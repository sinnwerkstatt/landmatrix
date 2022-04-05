import sys

import environ
from django.utils.translation import gettext_lazy as _

BASE_DIR = environ.Path(__file__) - 3  # type: environ.Path

env = environ.Env()
env.read_env(BASE_DIR(".env"))

LANGUAGE_CODE = "en"
WAGTAIL_CONTENT_LANGUAGES = LANGUAGES = [
    ("en", _("English")),
    ("es", _("Español")),
    ("fr", _("Français")),
    ("ru", _("Русский")),
]

TIME_ZONE = "Europe/Berlin"
WAGTAIL_I18N_ENABLED = USE_I18N = True
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
    "django.contrib.gis",
    # wagtail and dependencies
    "wagtail.contrib.modeladmin",
    "wagtail.contrib.forms",
    "wagtail.contrib.redirects",
    "wagtail.contrib.settings",
    # "wagtail.contrib.styleguide",
    "wagtail.embeds",
    "wagtail.sites",
    "wagtail.users",
    "wagtail.snippets",
    "wagtail.documents",
    "wagtail.images",
    "wagtail.search",
    "wagtail.admin",
    "wagtail.core",
    "wagtailorderable",
    "apps.blog",  # why here and not below?
    "modelcluster",
    "taggit",
    # 'treebeard',
    "wkhtmltopdf",
    "captcha",
    "rest_framework",
    "rest_framework.authtoken",
    "rest_framework_gis",
    "django.contrib.syndication",
    "file_resubmit",
    #   apps of the actual landmatrix project
    "apps.message",
    "apps.landmatrix",
    "apps.editor",
    "apps.wagtailcms",
    "apps.notifications",
    "impersonate",
    "celery",
    # green new deal
    "wagtail.api.v2",
    "ariadne_django",
    "corsheaders",
    "wagtailfontawesomesvg",
]

MIDDLEWARE = [
    # "django.middleware.cache.UpdateCacheMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    # wagtail and dependencies
    "wagtail.contrib.redirects.middleware.RedirectMiddleware",
    "impersonate.middleware.ImpersonateMiddleware",
    # "django.middleware.cache.FetchFromCacheMiddleware",
]

DEFAULT_AUTO_FIELD = "django.db.models.AutoField"

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
                "django.template.context_processors.i18n",
                "django.template.context_processors.media",
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
STATICFILES_DIRS = [
    BASE_DIR("frontend", "dist"),
]
STATICFILES_STORAGE = "django.contrib.staticfiles.storage.ManifestStaticFilesStorage"

FILE_UPLOAD_PERMISSIONS = 0o644

DATA_UPLOAD_MAX_MEMORY_SIZE = 4 * 1024 * 1024 * 1024
DATA_UPLOAD_MAX_NUMBER_FIELDS = None

LOCALE_PATHS = [BASE_DIR("config/locale")]

CACHES = {
    "default": env.cache("DJANGO_CACHE_URL", default="dummycache://"),
    "file_resubmit": {
        "BACKEND": "django.core.cache.backends.filebased.FileBasedCache",
        "LOCATION": "/tmp/file_resubmit/",
    },
}

CORS_ALLOWED_ORIGINS = [
    "https://dev.accountability.landmatrix.org",
    "https://accountability.landmatrix.org",
    "http://localhost:3000",
]
CORS_ALLOW_CREDENTIALS = True


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
    "REDIRECT_FIELD_NAME": "next",
}


# CELERY SETTINGS
BROKER_URL = "redis://localhost:6379/0"
CELERY_REDIS_BACKEND = BROKER_URL
CELERY_NAME = "landmatrix"

BLOG_LIMIT_AUTHOR_CHOICES_GROUP = "CMS Global (Editors)"

# django-registration
ACCOUNT_ACTIVATION_DAYS = 7

WKHTMLTOPDF_CMD = env("DJANGO_WKHTMLTOPDF_CMD", default="wkhtmltopdf")

ALLOWED_HOSTS = env.list("DJANGO_ALLOWED_HOSTS", default=["127.0.0.1", "localhost"])

LANDMATRIX_INVESTOR_GRAPH_ENABLED = True

TWITTER_TIMELINE = (
    {
        "consumer_key": env("DJANGO_TWITTER_CONSUMER_KEY"),
        "consumer_secret": env("DJANGO_TWITTER_CONSUMER_SECRET"),
        "access_token": env("DJANGO_TWITTER_ACCESS_TOKEN"),
        "access_token_secret": env("DJANGO_TWITTER_ACCESS_TOKEN_SECRET"),
    }
    if env("DJANGO_TWITTER_CONSUMER_KEY", default="")
    else None
)

TWITTER_DEFAULT_USERNAME = "land_matrix"
TWITTER_DEFAULT_COUNT = 5
