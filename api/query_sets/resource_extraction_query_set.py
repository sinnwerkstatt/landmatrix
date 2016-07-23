from django.utils.translation import ugettext_lazy as _

from api.query_sets.simple_fake_query_set import SimpleFakeQuerySet

class ResourceExtractionQuerySet(SimpleFakeQuerySet):
    def all(self):
        pass
