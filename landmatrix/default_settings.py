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
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'django.contrib.humanize',

#   works with django 1.8, not in 1.7:
#    'django.contrib.postgres',
    'django_hstore',

    'rest_framework',

    'tastypie',

# this apparently messes up the URL lookup in collaboration with cms. maybe try including it after cms.
#    'debug_toolbar',

#   django-cms and dependencies
    'cms',
    'mptt',
    'menus',
    'treebeard',
    'djangocms_admin_style',  # for the admin skin. You **must** add 'djangocms_admin_style' in the list **before** 'django.contrib.admin'.
    'django.contrib.admin',
    'django.contrib.sites',
    'sekizai',

#    'django-nose',

    'landmatrix',
    'global_app',
    'api'
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
#   added by generating the project with django 1.8, does not work in 1.7:
#    'django.middleware.security.SecurityMiddleware',

    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.doc.XViewMiddleware',
    'cms.middleware.user.CurrentUserMiddleware',
    'cms.middleware.page.CurrentPageMiddleware',
    'cms.middleware.toolbar.ToolbarMiddleware',
    'cms.middleware.language.LanguageCookieMiddleware',
)

ROOT_URLCONF = 'landmatrix.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
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
]

TIME_ZONE = 'Europe/Berlin'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/
STATIC_ROOT = os.path.join(BASE_DIR, "static")
STATIC_URL = '/static/'

MEDIA_ROOT = os.path.join(BASE_DIR, "media")
MEDIA_URL = "/media/"

#
# django REAT framework stuff
#
REST_FRAMEWORK = {
#    'DEFAULT_PERMISSION_CLASSES': ('rest_framework.permissions.IsAdminUser',),
    'PAGE_SIZE': 100
}

#
# tastypie
#
API_LIMIT_PER_PAGE = 100

#
# django-cms stuff
#
SITE_ID = 1

from django.conf.global_settings import TEMPLATE_CONTEXT_PROCESSORS as TCP

TEMPLATE_CONTEXT_PROCESSORS = TCP + (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'django.core.context_processors.request',
    'django.contrib.messages.context_processors.messages',
    'sekizai.context_processors.sekizai',
    'cms.context_processors.cms_settings',
)

TEMPLATE_DIRS = (
    os.path.join(BASE_DIR, "templates"),
)

CMS_TEMPLATES = (
    ('1-column.html', '1 column'),
    ('start.html', 'Start'),
)

