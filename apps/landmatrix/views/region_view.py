from django.http import Http404
from django.views.generic.base import View

from apps.wagtailcms.models import RegionIndex, RegionPage


class RegionView(View):
    def get(self, *args, **kwargs):
        try:
            region = RegionPage.objects.get(slug=kwargs.get("region_slug"))
        except RegionPage.DoesNotExist:
            try:
                region = RegionIndex.objects.get(slug="region")
            except RegionIndex.DoesNotExist:
                raise Http404("Region index not found.")

        return region.serve(self.request)
