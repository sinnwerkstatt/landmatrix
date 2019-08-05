from django.apps import AppConfig
from collections import OrderedDict


class GridConfig(AppConfig):
    name = 'grid'
    verbose_name = "Grid"

    VARIABLES = None

    def ready(self):
        pass
