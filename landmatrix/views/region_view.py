from django.http import Http404
from django.views.generic.base import View


from wagtailcms.models import RegionIndex, RegionPage


class RegionView(View):

    def get(self, *args, **kwargs):
        region_slug = kwargs.get('region_slug')
        if region_slug:
            try:
                region = RegionPage.objects.get(slug=region_slug)
            except RegionPage.DoesNotExist:
                raise Http404('Region not found.')
        else:
            try:
                region = RegionIndex.objects.get(slug='region')
            except RegionIndex.DoesNotExist:
                raise Http404('Region index not found.')

        return region.serve(self.request)
