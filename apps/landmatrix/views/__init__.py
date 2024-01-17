from django.conf import settings
from django.contrib import messages
from django.shortcuts import render
from django.utils.translation import gettext_lazy as _
from django.views.generic.base import RedirectView
from rest_framework import permissions, viewsets

from apps.landmatrix.models import FieldDefinition
from apps.landmatrix.models.country import Country, Region
from apps.landmatrix.models.currency import Currency
from apps.landmatrix.serializers import (
    FieldDefinitionSerializer,
    CurrencySerializer,
    CountrySerializer,
    RegionSerializer,
)


class SwitchLanguageView(RedirectView):
    permanent = False

    def get(self, request, language=None, *args, **kwargs):
        if language and language in dict(settings.LANGUAGES).keys():
            request.session["_language"] = language
            request.session["django_language"] = language
            request.LANGUAGE_CODE = language
        else:
            messages.error(request, _('The language "%s" is not supported' % language))

        return super(SwitchLanguageView, self).get(request, *args, **kwargs)

    def get_redirect_url(self, **kwargs):
        return self.request.GET.get("next", self.request.META.get("HTTP_REFERER", "/"))


def handler500(request):
    response = render(request, template_name="500.html")
    response.status_code = 500
    return response


class FieldDefinitionViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = FieldDefinition.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = FieldDefinitionSerializer


class CurrencyViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Currency.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = CurrencySerializer


class CountryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Country.objects.all().prefetch_related("deals")
    permission_classes = [permissions.AllowAny]
    serializer_class = CountrySerializer


class RegionViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Region.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = RegionSerializer
