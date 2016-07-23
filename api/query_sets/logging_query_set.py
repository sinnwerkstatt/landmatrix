from django.utils.translation import ugettext_lazy as _

from api.query_sets.simple_fake_query_set import SimpleFakeQuerySet

class LoggingQuerySet(SimpleFakeQuerySet):
    def all(self):
        pass
