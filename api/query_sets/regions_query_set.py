from api.query_sets.simple_fake_query_set import SimpleFakeQuerySet
from wagtailcms.models import RegionPage
from landmatrix.models.region import Region


class RegionsQuerySet(SimpleFakeQuerySet):
    def all(self):
        regions = RegionPage.objects.all().order_by('title')
        return [[region.region.id, region.region.slug, region.title] for region in regions]