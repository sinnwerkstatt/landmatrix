from api.query_sets.simple_fake_query_set import SimpleFakeQuerySet
from wagtailcms.models import RegionPage
from landmatrix.models import Region

__author__ = 'Lene Preuss <lp@sinnwerkstatt.com>'


class RegionsQuerySet(SimpleFakeQuerySet):
    def all(self):
        regions = Region.objects.all().order_by('name')
        return [[region.id, region.slug, region.name] for region in regions]