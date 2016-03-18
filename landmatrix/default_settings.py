"""
Django settings for landmatrix project.

Generated by 'django-admin startproject' using Django 1.8.2.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.8/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

FRONTENDDEV = False

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.8/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '#kzlezlh%t2o$c(^y=k^w@x3+jua*r8w2i)45xb(8ezpw_tdan'

ALLOWED_HOSTS = []

# Application definition

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages'
)

if FRONTENDDEV:
    # Needs to be added in this order.
    INSTALLED_APPS += (
        'django_gulp',
        'livereload'
    )

# Rest of the pack

INSTALLED_APPS += (
    'django.contrib.staticfiles',

    'django.contrib.humanize',

    'django.contrib.postgres',
    'django_hstore',

    'tastypie',

    # 'debug_toolbar',

    # wagtail and dependencies
    'wagtail.wagtailforms',
    'wagtail.wagtailredirects',
    'wagtail.wagtailembeds',
    'wagtail.wagtailsites',
    'wagtail.wagtailusers',
    'wagtail.wagtailsnippets',
    'wagtail.wagtaildocs',
    'wagtail.wagtailimages',
    'wagtail.wagtailsearch',
    'wagtail.wagtailadmin',
    'wagtail.wagtailcore',

    'modelcluster',
    'compressor',
    'taggit',

    'django.contrib.admin',
    'django.contrib.sites',
    'treebeard',

#   to check test coverage
    'coverage',
    'django.contrib.gis',
    'simple_history',
    'django_extensions',
    'crispy_forms',
    'wkhtmltopdf',
    'threadedcomments',
    'django_comments',

#   apps of the actual landmatrix project
    'landmatrix',
    'grid',
    'map',
    'charts',
    'editor',
    'wagtailcms',
    'api',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',

    # populate the history user automatically
    'simple_history.middleware.HistoryRequestMiddleware',

    'django.middleware.locale.LocaleMiddleware',
    # 'django.middleware.doc.XViewMiddleware',
    #'cms.middleware.user.CurrentUserMiddleware',
    #'cms.middleware.page.CurrentPageMiddleware',
    #'cms.middleware.toolbar.ToolbarMiddleware',
    #'cms.middleware.language.LanguageCookieMiddleware'

    # wagtail and dependencies
    'wagtail.wagtailcore.middleware.SiteMiddleware',
    'wagtail.wagtailredirects.middleware.RedirectMiddleware',
)

if FRONTENDDEV:
    MIDDLEWARE_CLASSES += 'livereload.middleware.LiveReloadScript',

ROOT_URLCONF = 'landmatrix.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, "templates")],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.contrib.auth.context_processors.auth',
                'django.core.context_processors.i18n',
                'django.core.context_processors.media',
                'django.core.context_processors.static',
                'django.core.context_processors.request',
                'django.contrib.messages.context_processors.messages',
                'sekizai.context_processors.sekizai',
                'wagtailcms.context_processors.add_root_page',
            ],
        },
    },
]

WSGI_APPLICATION = 'landmatrix.wsgi.application'

# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/

LANGUAGE_CODE = 'en'
LANGUAGES = [
    ('en', 'English'),
    ('de', 'Deutsch'),
    ('es', 'Espagnol'),
]

TIME_ZONE = 'Europe/Berlin'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/
STATIC_ROOT = os.path.join(BASE_DIR, "static")
STATIC_URL = '/static/'

#STATICFILES_DIRS = (
#    os.path.join(BASE_DIR, "landmatrix", "static", "vendor"),
#)

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'compressor.finders.CompressorFinder'
)

MEDIA_ROOT = os.path.join(BASE_DIR, "media")
MEDIA_URL = "/media/"

#
# tastypie
#
API_LIMIT_PER_PAGE = 100

#
# django-cms stuff
#
SITE_ID = 1

CMS_TEMPLATES = (
    ('1-column.html', '1 column'),
    ('start.html', 'Start'),
    ('base-gettheidea.html', 'Get the idea'),
    ('base-map.html', 'Map'),
)

# CMS Editor (ckeditor)

CKEDITOR_SETTINGS = {
    'toolbar': 'CMS',
    'skin': 'moono',
    'stylesSet': [
        {'name': 'Panel', 'element': 'div', 'class': 'panel-lm'}
    ]
}

DEBUG_TOOLBAR_PANELS = [
    'debug_toolbar.panels.versions.VersionsPanel',
    'debug_toolbar.panels.timer.TimerPanel',
    'debug_toolbar.panels.settings.SettingsPanel',
    'debug_toolbar.panels.headers.HeadersPanel',
    'debug_toolbar.panels.request.RequestPanel',
    'debug_toolbar.panels.sql.SQLPanel',
    'debug_toolbar.panels.templates.TemplatesPanel',
    'debug_toolbar.panels.cache.CachePanel',
    'debug_toolbar.panels.signals.SignalsPanel',
    'debug_toolbar.panels.logging.LoggingPanel',
    'debug_toolbar.panels.profiling.ProfilingPanel',
    'debug_toolbar_line_profiler.panel.ProfilingPanel'
]

# enable persistent database connections
# (https://docs.djangoproject.com/en/1.9/ref/databases/#persistent-database-connections)
CONN_MAX_AGE = 0

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
    }
}

COMMENTS_APP = 'threadedcomments'

WAGTAIL_SITE_NAME = 'Land Matrix'
