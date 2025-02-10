from django.apps import AppConfig


class LandMatrixConfig(AppConfig):
    name = "apps.landmatrix"
    verbose_name = "Land Matrix"

    def ready(self):
        from apps.landmatrix import signals  # noqa: F401
