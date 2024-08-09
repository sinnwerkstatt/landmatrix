from django.db import models
from django.db.models import Q, QuerySet, F
from django.db.models.functions import JSONObject
from django.http import Http404

from apps.accounts.models import User
from apps.landmatrix.models.abstract.hull import BaseHull


class InvestorHullQuerySet(models.QuerySet):
    def normal(self):
        return self.filter(deleted=False)

    def active(self):
        return self.normal().filter(active_version__isnull=False)

    # NOTE at the moment the only thing we filter on is the "status".
    # the following is an idea:
    # def public(self):
    #     return self.active().filter(is_actually_unknown=False)

    def visible(self, user=None, subset="PUBLIC"):
        if subset in ["ACTIVE", "PUBLIC"]:
            return self.active()

        if not user or not user.is_authenticated:
            return self.active()

        # hand it out unfiltered.
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


class InvestorHull(BaseHull):
    active_version = models.ForeignKey(
        "InvestorVersion",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="+",
    )
    draft_version = models.ForeignKey(
        "InvestorVersion",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="+",
    )

    objects = InvestorHullQuerySet.as_manager()

    def __str__(self):
        return f"#{self.id}"

    # This method is used by DRF.
    def selected_version(self):
        if hasattr(self, "_selected_version_id") and self._selected_version_id:
            from apps.landmatrix.models.investor import InvestorVersion

            try:
                return self.versions.get(id=self._selected_version_id)
            except InvestorVersion.DoesNotExist:
                raise Http404
        return self.active_version or self.draft_version

    def add_draft(self, created_by: User = None) -> "InvestorVersion":
        from apps.landmatrix.models.investor import InvestorVersion

        dv = InvestorVersion.objects.create(investor=self, created_by=created_by)
        self.draft_version = dv
        self.save()
        return dv

    # This method is used by DRF.
    def involvements(self):
        if not hasattr(self, "_selected_version_id") and self.active_version:
            from apps.landmatrix.models.investor import Involvement

            return Involvement.objects.filter(
                Q(parent_investor_id=self.id) | Q(child_investor_id=self.id)
            )
        return

    def involvements_graph(self, depth, include_deals, show_ventures):
        from apps.landmatrix.involvement_network import InvolvementNetwork

        return InvolvementNetwork().get_network_x(
            self.id, depth, include_deals=include_deals, show_ventures=show_ventures
        )

    def to_list_dict(self):
        """
        should only be called on InvestorHulls filtered by having active_versions
        """
        return {
            "id": self.id,
            "selected_version": {
                "id": self.active_version.id,
                "name": self.active_version.name,
                "modified_at": self.active_version.modified_at,
                "classification": self.active_version.classification,
                "country": {"id": self.active_version.country_id},
            },
        }

    @staticmethod
    def to_investor_list(qs: QuerySet["InvestorHull"]):
        from apps.landmatrix.models.deal import DealHull

        deals = DealHull.objects.filter(
            active_version__operating_company_id__in=qs.values_list("id", flat=True)
        ).values("id", "active_version__operating_company_id")

        return [
            {
                "id": inv["id"],
                "selected_version": inv["selected_version"],
                "deals": [
                    x["id"]
                    for x in deals
                    if x["active_version__operating_company_id"] == inv["id"]
                ],
            }
            for inv in qs.annotate(
                selected_version=JSONObject(
                    id="active_version_id",
                    name="active_version__name",
                    name_unknown="active_version__name_unknown",
                    modified_at="active_version__modified_at",
                    classification="active_version__classification",
                    country_id="active_version__country_id",
                )
            ).values("id", "selected_version")
        ]

    def get_parent_companies(
        self, top_investors_only=False, _seen_investors: set["InvestorHull"] = None
    ) -> set["InvestorHull"]:
        """
        Get list of the highest parent companies
        (all right-hand side parent companies of the network visualisation)
        """
        if _seen_investors is None:
            _seen_investors = {self}

        from apps.landmatrix.models.investor import Involvement

        investor_involvements = (
            Involvement.objects.filter(child_investor=self)
            .filter(
                parent_investor__active_version__isnull=False,
                parent_investor__deleted=False,
            )
            .filter(role="PARENT")
            .exclude(parent_investor__in=_seen_investors)
        )

        self.is_top_investor = not investor_involvements

        for involvement in investor_involvements:
            if involvement.parent_investor in _seen_investors:
                continue
            _seen_investors.add(involvement.parent_investor)
            involvement.parent_investor.get_parent_companies(
                top_investors_only, _seen_investors
            )
        return _seen_investors

    def get_affected_dealversions(self, seen_investors=None) -> set["DealVersion"]:
        """
        Get list of affected deals - this is like Top Investors, only downwards
        (all left-hand side deals of the network visualisation)
        """

        from apps.landmatrix.models.deal import DealVersion

        deals = set()
        if seen_investors is None:
            seen_investors = {self}

        child_investor_involvements = (
            self.child_investors.active()
            .filter(role="PARENT")
            .exclude(child_investor__in=seen_investors)
        )

        dealv: DealVersion
        for dealv in self.dealversions.filter(id=F("deal__active_version_id")):
            deals.add(dealv)

        for involvement in child_investor_involvements:
            if involvement.child_investor in seen_investors:
                continue
            seen_investors.add(involvement.child_investor)
            deals.update(
                involvement.child_investor.get_affected_dealversions(seen_investors)
            )
        return deals
