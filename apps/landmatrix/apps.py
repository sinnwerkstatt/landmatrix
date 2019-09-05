from django.apps import AppConfig


class LandMatrixConfig(AppConfig):
    name = 'apps.landmatrix'
    verbose_name = "Land Matrix"

    def ready(self):
        # noinspection PyUnresolvedReferences
        from apps.landmatrix import signals
