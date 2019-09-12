from django.apps import AppConfig


class NotificationsConfig(AppConfig):
    name = 'apps.notifications'
    verbose_name = "Notifications"

    def ready(self):
        # noinspection PyUnresolvedReferences
        from apps.notifications import signals
