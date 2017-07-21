from django.apps import AppConfig


class LandMatrixConfig(AppConfig):
    name = 'landmatrix'
    verbose_name = "Land Matrix"

    def ready(self):
        from landmatrix import signals

