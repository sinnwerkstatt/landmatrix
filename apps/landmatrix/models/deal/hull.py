from django.db import models
from django.db.models import Count, Func, F
from django.http import Http404
from django.utils.translation import gettext as _

from apps.accounts.models import User
from apps.landmatrix.models.abstract.hull import BaseHull
from apps.landmatrix.models.country import Country


class DealHullQuerySet(models.QuerySet):
    def normal(self):
        return self.filter(deleted=False)

    def active(self):
        return self.normal().filter(active_version__isnull=False)

    def public(self):
        return self.active().filter(active_version__is_public=True, confidential=False)

    def visible(self, user=None, subset="PUBLIC"):
        # TODO Later: welche user duerfen unfiltered bekommen?
        if not user or not user.is_authenticated:
            return self.public()

        if subset == "PUBLIC":
            return self.public()
        elif subset == "ACTIVE":
            return self.active()
        return self.normal()

    # def with_mode(self):
    #     return self.annotate(
    #         mode=Case(
    #             When(
    #                 ~Q(active_version_id=None) & ~Q(draft_version_id=None),
    #                 then=Concat(Value("ACTIVE + "), "draft_version__status"),
    #             ),
    #             When(
    #                 ~Q(active_version_id=None) & Q(draft_version_id=None),
    #                 then=Value("ACTIVE"),
    #             ),
    #             When(
    #                 Q(active_version_id=None) & ~Q(draft_version_id=None),
    #                 then="draft_version__status",
    #             ),
    #             default=Value(""),
    #         )
    #     )


class DealHull(BaseHull):
    country = models.ForeignKey(
        Country,
        verbose_name=_("Target country"),
        on_delete=models.PROTECT,
        blank=True,
        null=True,
        related_name="deals",
    )

    active_version = models.ForeignKey(
        "DealVersion",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="+",
    )
    draft_version = models.ForeignKey(
        "DealVersion",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="+",
    )

    confidential = models.BooleanField(default=False)
    confidential_comment = models.TextField(
        _("Comment why this deal is private"), blank=True
    )

    # ## calculated
    fully_updated_at = models.DateTimeField(
        _("Last full update"), null=True, blank=True
    )

    objects = DealHullQuerySet.as_manager()

    def __str__(self):
        if self.country:
            return f"#{self.id} in {self.country.name}"
        return f"#{self.id}"

    def selected_version(self):
        if hasattr(self, "_selected_version_id") and self._selected_version_id:
            from apps.landmatrix.models.deal import DealVersion

            try:
                return self.versions.get(id=self._selected_version_id)
            except DealVersion.DoesNotExist:
                raise Http404
        return self.active_version or self.draft_version

    def add_draft(self, created_by: User = None) -> "DealVersion":
        from apps.landmatrix.models.deal import DealVersion

        dv = DealVersion.objects.create(deal=self, created_by=created_by)
        self.draft_version = dv
        self.save()
        return dv

    @classmethod
    def get_geo_markers(cls, region_id=None, country_id=None):
        deals = cls.objects.public().exclude(country=None)
        if region_id:
            return [
                {
                    "country_id": x["country_id"],
                    "count": x["count"],
                    "coordinates": [x["country__point_lat"], x["country__point_lon"]],
                }
                for x in deals.filter(country__region_id=region_id)
                .values("country_id", "country__point_lat", "country__point_lon")
                .annotate(count=Count("pk"))
                # .annotate(size=Sum("deal_size"))
            ]
        if country_id:
            xx = [
                {"coordinates": x}
                for x in deals.filter(country_id=country_id)
                .filter(active_version__locations__point__isnull=False)
                .annotate(
                    point_lat=Func(
                        "active_version__locations__point",
                        function="ST_Y",
                        output_field=models.FloatField(),
                    ),
                    point_lng=Func(
                        "active_version__locations__point",
                        function="ST_X",
                        output_field=models.FloatField(),
                    ),
                )
                .values_list("point_lat", "point_lng")
            ]
            return xx

        region_coordinates = {
            2: [6.06433, 17.082249],
            9: [-22.7359, 140.0188],
            21: [54.526, -105.2551],
            142: [34.0479, 100.6197],
            150: [52.0055, 37.9587],
            419: [-4.442, -61.3269],
        }
        return [
            {
                "region_id": x["region_id"],
                "count": x["count"],
                "coordinates": region_coordinates[x["region_id"]],
            }
            for x in deals.values(region_id=F("country__region_id")).annotate(
                count=Count("pk")
            )
        ]
