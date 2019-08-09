import os

import environ
from django.utils.translation import ugettext_lazy as _

BASE_DIR = environ.Path(__file__) - 3  # type: environ.Path


env = environ.Env()
env.read_env(BASE_DIR('.env'))

LANGUAGE_CODE = 'en'
LANGUAGES = [
    ('en', _('English')),
    ('es', _('Español')),
    ('fr', _('Français')),
]
TIME_ZONE = 'Europe/Berlin'
USE_I18N = True
USE_L10N = True
USE_TZ = True
SITE_ID = 1


ROOT_URLCONF = 'config.urls'
WSGI_APPLICATION = 'config.wsgi.application'


EMAIL_CONFIG = env.email_url('DJANGO_EMAIL_URL', default='consolemail://')
vars().update(EMAIL_CONFIG)
SERVER_EMAIL = EMAIL_CONFIG['EMAIL_HOST_USER']
DEFAULT_FROM_EMAIL = SERVER_EMAIL

DATABASES = {'default': env.db("DATABASE_URL")}

INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    #'django.contrib.staticfiles',
    'django.contrib.humanize',
    'django.contrib.postgres',
    'wagtail_modeltranslation',
    'wagtail_modeltranslation.makemigrations',
    'wagtail_modeltranslation.migrate',
    'django.contrib.admin',
    'django.contrib.sites',

    # OL3 widgets must come before GIS
    'ol3_widgets',
    'django.contrib.gis',
    # 'django_hstore',

    # 'tastypie',

    # wagtail and dependencies
    'wagtail.contrib.forms',
    'wagtail.contrib.redirects',
    'wagtail.embeds',
    'wagtail.sites',
    'wagtail.users',
    'wagtail.snippets',
    'wagtail.documents',
    'wagtail.images',
    'wagtail.search',
    'wagtail.admin',
    'wagtail.core',
    'blog',

    'modelcluster',
    'compressor',
    'taggit',

    'sass_processor',
    # 'sekizai',

    'bootstrap3_datetime',

    'treebeard',

    'jstemplate',

    'simple_history',
    # 'django_extensions',
    'crispy_forms',
    'wkhtmltopdf',
    'threadedcomments',
    'django_comments',
    'captcha',
    'rest_framework',
    'rest_framework.authtoken',
    'rest_framework_gis',
    # 'rest_framework_docs',
    'rest_framework_swagger',
    'django.contrib.syndication',
    'file_resubmit',

    #   apps of the actual landmatrix project
    'message',
    'landmatrix',
    'grid',
    'map',
    'charts',
    'editor',
    'wagtailcms',
    'api',
    'notifications',
    'public_comments',
    'feeds',
    'impersonate',
    'celery',
]

MIDDLEWARE = [
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',

    # populate the history user automatically
    'simple_history.middleware.HistoryRequestMiddleware',

    # FIXME: Temp. disabled because there's just one language in the frontend
    # 'django.middleware.locale.LocaleMiddleware',

    # wagtail and dependencies
    'wagtail.core.middleware.SiteMiddleware',
    'wagtail.contrib.redirects.middleware.RedirectMiddleware',
    'impersonate.middleware.ImpersonateMiddleware',
]

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR("templates")],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.i18n',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.template.context_processors.request',
                'django.contrib.messages.context_processors.messages',
                # 'sekizai.context_processors.sekizai',
                'wagtailcms.context_processors.add_root_page',
                'wagtailcms.context_processors.add_data_source_dir',
                'wagtailcms.context_processors.add_countries_and_regions',
                'message.context_processors.add_custom_messages'
            ],
        },
    },
]

LOGIN_REDIRECT_URL = '/editor/'
# Limit all uploads to 20MB, and data sources to 1MB
MAX_UPLOAD_SIZE = 20971520
DATA_SOURCE_MAX_UPLOAD_SIZE = 10485760
DATA_SOURCE_DIR = 'uploads'  # appended to MEDIA_ROOT/MEDIA_URL


MEDIA_ROOT = BASE_DIR('media')
MEDIA_URL = '/media/'
STATIC_ROOT = BASE_DIR('static-collected')
STATIC_URL = '/static/'
# STATICFILES_FINDERS = (
#     'django.contrib.staticfiles.finders.FileSystemFinder',
#     'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#     'compressor.finders.CompressorFinder',
#     'sass_processor.finders.CssFinder'
# )
STATICFILES_DIRS = [
    BASE_DIR('node_modules'),
]

FILE_UPLOAD_PERMISSIONS = 0o644

# SASS_PATH = os.path.join(BASE_DIR, 'static/css'),

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
    },
    "file_resubmit": {
        'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
        "LOCATION": '/tmp/file_resubmit/'
    },
}

COMMENTS_APP = 'public_comments'

WAGTAIL_SITE_NAME = 'Land Matrix'

MODELTRANSLATION_CUSTOM_FIELDS = ('NoWrapsStreamField',)

# Django REST Framework settings
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    )
}

IMPERSONATE = {
    "REDIRECT_URL": '/editor/',
    "REQUIRE_SUPERUSER": True,
    "ALLOW_SUPERUSER": True
}

ELASTICSEARCH_URL = env('ELASTICSEARCH_URL', default='http://localhost')
ELASTICSEARCH_INDEX_NAME = 'landmatrix'

# CELERY SETTINGS
BROKER_URL = 'redis://localhost:6379/0'
CELERY_REDIS_BACKEND = BROKER_URL
CELERY_NAME = 'landmatrix'


BLOG_LIMIT_AUTHOR_CHOICES_GROUP = 'CMS Global (Editors)'

# django-registration
ACCOUNT_ACTIVATION_DAYS = 7

WKHTMLTOPDF_CMD = env('DJANGO_WKHTMLTOPDF_CMD', default=None)

ALLOWED_HOSTS = env.list('DJANGO_ALLOWED_HOSTS', default=['127.0.0.1', 'localhost'])

# TODO: Remove this settings from code
CONVERT_DB = False
CONVERT_FROM_MY = False
TEST_AGAINST_LIVE_DB = False