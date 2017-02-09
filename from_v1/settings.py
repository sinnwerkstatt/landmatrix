
# whether to show SQL generated (is referenced below when configuring logging)
LOG_DB_QUERIES = False

CONVERT_DB = True
CONVERT_FROM_MY = True
TEST_AGAINST_LIVE_DB = False

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

MAX_UPLOAD_SIZE = "5242880"

# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases
DATABASES = {
    'default': {
#        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': 'landmatrix_2',                         # CORRECT DB FOR V2 GOES HERE
        'USER': 'landmatrix',
        'PASSWORD': 'landmatrix',
        'HOST': '',
        'PORT': '5433',
    },
}
if CONVERT_DB:
    DATABASES['v2'] = DATABASES['default']
    if CONVERT_FROM_MY:
        DATABASES['v1_my'] = {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': 'landmatrix_1',                     # CORRECT DB FOR V1 GOES HERE
            'USER': 'root',
            'PASSWORD': 'moin',
            'HOST': '',
            'PORT': '3306',
        }
    else:
        DATABASES['v1_pg'] = {
            'ENGINE': 'django.db.backends.postgresql_psycopg2', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
            'NAME': 'landmatrix_1',                     # CORRECT DB FOR V1 GOES HERE
            'USER': 'root',
            'PASSWORD': 'moin',
            'HOST': '',
            'PORT': '5433',
        }
    DATABASES['lo'] = {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': 'lo_data',  # CORRECT DB FOR LAND OBSERVATORY GOES HERE
        'USER': 'landmatrix',
        'PASSWORD': 'landmatrix',
        'HOST': '',
        'PORT': '5433',
    }

if LOG_DB_QUERIES:
    LOGGING = {
        'version': 1,
        'filters': {
            'require_debug_true': {
                '()': 'django.utils.log.RequireDebugTrue',
            }
        },
        'handlers': {
            'console': {
                'level': 'DEBUG',
                'filters': ['require_debug_true'],
                'class': 'logging.StreamHandler',
            }
        },
        'loggers': {
            'django.db.backends': {
                'level': 'DEBUG',
                'handlers': ['console'],
            }
        }
    }

from .default_settings import *

INSTALLED_APPS += (
    'debug_toolbar',
)
MIDDLEWARE_CLASSES += (
    # ...
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    # ...
)

DEBUG_TOOLBAR_CONFIG = {
    'PROFILER_MAX_DEPTH': 16
}