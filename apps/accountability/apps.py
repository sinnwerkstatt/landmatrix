from django.apps import AppConfig


class AccountabilityConfig(AppConfig):
    name = "apps.accountability"
    default_auto_field = "django.db.models.BigAutoField"

    def ready(self):
        import apps.accountability.signals  # noqa: F401
