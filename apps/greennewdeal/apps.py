from django.apps import AppConfig


class GreenNewDealConfig(AppConfig):
    name = "apps.greennewdeal"
    verbose_name = "GreenNewDeal"

    def ready(self):
        # noinspection PyUnresolvedReferences
        from apps.greennewdeal import signals
