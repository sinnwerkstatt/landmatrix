from django.conf import settings
from django.contrib import messages
from django.db.models import Prefetch
from django.shortcuts import render
from django.utils.translation import gettext_lazy as _
from django.views.generic.base import RedirectView
from rest_framework import permissions, viewsets
from rest_framework.mixins import ListModelMixin

from apps.landmatrix.models.country import Country, Region
from apps.landmatrix.models.currency import Currency
from apps.landmatrix.models.deal import DealHull
from apps.landmatrix.serializers import (
    CountrySerializer,
    CurrencySerializer,
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
            messages.error(
                request,
                _("Unsupported language: {language_code}").format(
                    language_code=language
                ),
            )

        return super().get(request, *args, **kwargs)

    def get_redirect_url(self, **kwargs):
        return self.request.GET.get("next", self.request.META.get("HTTP_REFERER", "/"))


def handler500(request):
    response = render(request, template_name="500.html")
    response.status_code = 500
    return response


class CurrencyViewSet(ListModelMixin, viewsets.GenericViewSet):
    queryset = Currency.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = CurrencySerializer


class CountryViewSet(ListModelMixin, viewsets.GenericViewSet):
    queryset = Country.objects.all().prefetch_related(
        # Only list public deals
        Prefetch("deals", queryset=DealHull.objects.public().order_by("id"))
    )
    permission_classes = [permissions.AllowAny]
    serializer_class = CountrySerializer


class RegionViewSet(ListModelMixin, viewsets.GenericViewSet):
    queryset = Region.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = RegionSerializer
