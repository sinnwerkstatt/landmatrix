from __future__ import absolute_import

from .celery_app import app as celery_app

__all__ = ("celery_app",)

default_app_config = "apps.landmatrix.apps.LandMatrixConfig"
