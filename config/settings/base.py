# noinspection PyPackageRequirements
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
DATABASES["default"]["OPTIONS"] = {"options": "-c statement_timeout=10000"}

INSTALLED_APPS = [
    # this must come first (before django.contrib.auth)
    "apps.accounts",
    # django
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.admin",
    "django.contrib.sites",
    "django.contrib.gis",
    # modeltranslation
    "wagtail_modeltranslation",
    "wagtail_modeltranslation.makemigrations",
    "wagtail_modeltranslation.migrate",
    # wagtail
    "wagtail.contrib.redirects",
    "wagtail.contrib.settings",
    "wagtail.embeds",
    "wagtail.sites",
    "wagtail.users",
    "wagtail.snippets",
    "wagtail.documents",
    "wagtail.images",
    "wagtail.search",
    "wagtail.admin",
    "wagtail",
    "wagtail.api.v2",
    "rest_framework",
    "rest_framework_gis",
    "drf_spectacular",
    "drf_spectacular_sidecar",
    "wagtailfontawesomesvg",
    "wagtailorderable",
    "modelcluster",
    "taggit",
    "wagtail_headless_preview",
    #   apps of the actual landmatrix project
    "apps.blog",
    "apps.message",
    "apps.landmatrix",
    "apps.wagtailcms",
    "apps.new_model",
    # plumbing
    "impersonate",
    "corsheaders",
]

MIDDLEWARE = [
    # "django.middleware.cache.UpdateCacheMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    # should be after SessionMiddleware and before CommonMiddleware
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

AUTH_USER_MODEL = "accounts.User"
WAGTAIL_USER_EDIT_FORM = "apps.accounts.forms.CustomUserEditForm"
WAGTAIL_USER_CREATION_FORM = "apps.accounts.forms.CustomUserCreationForm"
WAGTAIL_USER_CUSTOM_FIELDS = ["role", "country", "region"]

LOGIN_REDIRECT_URL = "/"
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
STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
    "staticfiles": {
        "BACKEND": "django.contrib.staticfiles.storage.ManifestStaticFilesStorage"
    },
}

FORMS_URLFIELD_ASSUME_HTTPS = True

FILE_UPLOAD_PERMISSIONS = 0o644

DATA_UPLOAD_MAX_MEMORY_SIZE = 4 * 1024 * 1024 * 1024
DATA_UPLOAD_MAX_NUMBER_FIELDS = None

LOCALE_PATHS = [BASE_DIR("config/locale")]

CACHES = {
    "default": env.cache("DJANGO_CACHE_URL", default="dummycache://"),
}

CORS_ALLOWED_ORIGINS = [
    "https://dev.accountability.landmatrix.org",
    "https://accountability.landmatrix.org",
]
CORS_ALLOW_CREDENTIALS = True

WAGTAIL_SITE_NAME = "Land Matrix"
WAGTAILADMIN_BASE_URL = "https://landmatrix.org"

WAGTAIL_HEADLESS_PREVIEW = {
    "CLIENT_URLS": {"default": "{SITE_ROOT_URL}/wagtail-preview"},
    "LIVE_PREVIEW": False,  # set to True to enable live preview functionality
    "SERVE_BASE_URL": None,  # can be used for HeadlessServeMixin
    "REDIRECT_ON_PREVIEW": False,
    # set to True to redirect to the preview instead of using the Wagtail default mechanism
}

# Django REST Framework settings
REST_FRAMEWORK = {
    "COERCE_DECIMAL_TO_STRING": False,
    "DEFAULT_AUTHENTICATION_CLASSES": (
        # "rest_framework.authentication.BasicAuthentication",
        "rest_framework.authentication.SessionAuthentication",
    ),
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
}
SPECTACULAR_SETTINGS = {
    "TITLE": "Land Matrix API",
    "DESCRIPTION": "The Land Matrix is an independent land monitoring initiative that promotes transparency and accountability.",
    "VERSION": "1.0.0",
    "SERVE_INCLUDE_SCHEMA": True,
    "SWAGGER_UI_DIST": "SIDECAR",
    "SWAGGER_UI_FAVICON_HREF": "SIDECAR",
    "REDOC_DIST": "SIDECAR",
    # "SERVE_URLCONF": "apps.api.urls",
    "PREPROCESSING_HOOKS": ["apps.api.spectacular.preprocessing_filter_spec"],
    # "SERVE_PUBLIC": False,
    "ENUM_NAME_OVERRIDES": {
        # Reuse enum instead of create a distinct one per choices field
        "HaAreasEnum": "apps.landmatrix.models.choices.HaAreasEnum",
        "BenefitsEnum": "apps.landmatrix.models.choices.BenefitsEnum",
        "CropsEnum": "apps.landmatrix.models.choices.CropsEnum",
        "AnimalsEnum": "apps.landmatrix.models.choices.AnimalsEnum",
        "MineralsEnum": "apps.landmatrix.models.choices.MineralsEnum",
    },
}

IMPERSONATE = {
    "REDIRECT_URL": "/editor/",
    "REQUIRE_SUPERUSER": True,
    "ALLOW_SUPERUSER": True,
    "REDIRECT_FIELD_NAME": "next",
}

BLOG_LIMIT_AUTHOR_CHOICES_GROUP = "CMS Global (Editors)"

ACCOUNT_ACTIVATION_DAYS = 7

ALLOWED_HOSTS = env.list("DJANGO_ALLOWED_HOSTS", default=["127.0.0.1", "localhost"])

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
