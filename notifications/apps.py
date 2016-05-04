from django.apps import AppConfig


class NotificationsConfig(AppConfig):
    name = 'notifications'
    verbose_name = "Notifications"

    def ready(self):
        from notifications import signals
