from django.http import Http404
from django.views.generic.base import View

from apps.wagtailcms.models import RegionIndex, RegionPage


class RegionView(View):
    def get(self, *args, **kwargs):
        try:
            region = RegionPage.objects.get(slug_en=kwargs.get("region_slug"))
        except RegionPage.DoesNotExist:
            try:
                region = RegionIndex.objects.get(slug_en="region")
            except RegionIndex.DoesNotExist:
                raise Http404("Region index not found.")

        return region.serve(self.request)
