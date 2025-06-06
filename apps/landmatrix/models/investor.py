import re

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models import Q, QuerySet
from django.db.models.functions import JSONObject
from django.http import Http404
from django.utils.translation import gettext as _

from apps.accounts.models import User
from apps.landmatrix.models import choices, schema
from apps.landmatrix.models.abstract import (
    BaseDataSource,
    BaseHull,
    BaseVersion,
    BaseWorkflowInfo,
    VersionStatus,
    VersionTransition,
)
from apps.landmatrix.models.choices import InvolvementRoleEnum
from apps.landmatrix.models.country import Country
from apps.landmatrix.models.currency import Currency
from apps.landmatrix.models.fields import (
    ChoiceArrayField,
    ChoiceField,
    LooseDateField,
    NanoIDField,
)
from apps.landmatrix.nid import generate_nid
from django_pydantic_jsonfield import PydanticJSONField, SchemaValidator


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
        verbose_name=_("Active version"),
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="+",
    )
    draft_version = models.ForeignKey(
        "InvestorVersion",
        verbose_name=_("Draft version"),
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
            try:
                return self.versions.get(id=self._selected_version_id)
            except InvestorVersion.DoesNotExist as e:
                raise Http404(
                    f"InvestorVersion {self._selected_version_id} does not exist."
                ) from e
        return self.active_version or self.draft_version

    def add_draft(self, created_by: User = None) -> "InvestorVersion":
        dv: InvestorVersion = InvestorVersion.objects.create(
            investor=self,
            created_by=created_by,
            modified_by=created_by,
        )
        self.draft_version = dv
        self.save()
        return dv

    # This method is used by DRF.
    def involvements(self):
        if not hasattr(self, "_selected_version_id") and self.active_version:
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

    def get_parents(self) -> "InvolvementQuerySet":
        # return self.parent_investors.all()
        return Involvement.objects.filter(child_investor=self)

    def get_children(self) -> "InvolvementQuerySet":
        # return self.child_investors.all()
        return Involvement.objects.filter(parent_investor=self)

    def get_involved_deal_versions(
        self,
        seen_investors: set["InvestorHull"] | None = None,
    ):
        """
        Get list of affected deals - this is like Top Investors, only downwards
        (all left-hand side deals of the network visualisation)
        """
        if seen_investors is None:
            seen_investors = {self}

        deal_versions = {*self.dealversions.all()}

        qs_involvements_as_parent = (
            self.get_children()
            .filter(role=InvolvementRoleEnum.PARENT)
            .exclude(child_investor_id__in=seen_investors)
        )

        for involvement in qs_involvements_as_parent:
            child_investor = involvement.child_investor

            seen_investors.add(child_investor)
            deal_versions.update(
                child_investor.get_involved_deal_versions(seen_investors)
            )

        return deal_versions


class InvolvementQuerySet(models.QuerySet):
    def active(self):
        return self.filter(
            parent_investor__active_version__isnull=False,
            parent_investor__deleted=False,
            child_investor__active_version__isnull=False,
            child_investor__deleted=False,
        )

    # this is just an idea at this point
    # def public(self):
    #     return self.active().filter(
    #         investor__is_actually_unknown=False,
    #         venture__is_actually_unknown=False,
    #     )

    def visible(self, user=None, subset="PUBLIC"):
        if subset in ["ACTIVE", "PUBLIC"]:
            return self.active()

        if not user or not (user.is_staff or user.is_superuser):
            return self.active()

        # hand it out unfiltered.
        return self


class Involvement(models.Model):
    nid = NanoIDField(_("ID"), max_length=15, db_index=True)

    parent_investor = models.ForeignKey(
        InvestorHull,
        verbose_name=_("Investor"),
        db_index=True,
        related_name="child_investors",
        on_delete=models.PROTECT,
    )
    child_investor = models.ForeignKey(
        InvestorHull,
        verbose_name=_("Venture Company"),
        db_index=True,
        related_name="parent_investors",
        on_delete=models.PROTECT,
    )
    role = models.CharField(
        _("Relation type"),
        choices=choices.INVOLVEMENT_ROLE_CHOICES,
    )
    investment_type = ChoiceArrayField(
        ChoiceField(choices.INVESTMENT_TYPE_CHOICES),
        verbose_name=_("Investment type"),
        blank=True,
        default=list,
    )
    percentage = models.DecimalField(
        _("Ownership share"),
        blank=True,
        null=True,
        max_digits=5,
        decimal_places=2,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
    )
    loans_amount = models.FloatField(
        _("Loan amount"),
        blank=True,
        null=True,
    )
    loans_currency = models.ForeignKey(
        Currency,
        verbose_name=_("Loan currency"),
        blank=True,
        null=True,
        on_delete=models.PROTECT,
    )
    loans_date = LooseDateField(
        _("Loan date"),
        blank=True,
        null=True,
    )
    parent_relation = ChoiceField(
        choices.PARENT_RELATION_CHOICES,
        verbose_name=_("Parent relation"),
    )
    comment = models.TextField(
        _("Comment on involvement"),
        blank=True,
    )

    objects = InvolvementQuerySet.as_manager()

    class Meta:
        verbose_name = _("Investor Venture Involvement")
        verbose_name_plural = _("Investor Venture Involvements")
        ordering = ["id"]
        unique_together = [["parent_investor", "child_investor"]]

    def __str__(self):
        if self.role == "PARENT":
            role = _("<is PARENT of>")
        else:
            role = _("<is INVESTOR of>")
        return f"{self.parent_investor} {role} {self.child_investor}"

    def save(self, *args, **kwargs):
        if self._state.adding and not self.nid:
            self.nid = generate_nid(Involvement)
        super().save(*args, **kwargs)


class InvestorVersion(BaseVersion):
    investor = models.ForeignKey(
        InvestorHull,
        verbose_name=_("Investor"),
        on_delete=models.PROTECT,
        related_name="versions",
    )

    name = models.CharField(_("Name"), blank=True)
    country = models.ForeignKey(
        Country,
        verbose_name=_("Country of registration/origin"),
        blank=True,
        null=True,
        on_delete=models.PROTECT,
    )
    classification = ChoiceField(
        choices.INVESTOR_CLASSIFICATION_CHOICES,
        verbose_name=_("Classification"),
    )
    homepage = models.URLField(_("Investor homepage"), blank=True)
    opencorporates = models.URLField(_("Opencorporates link"), blank=True)
    comment = models.TextField(_("Comment"), blank=True)

    # """ Data sources """  via Foreignkey

    # META
    ds_quotations = PydanticJSONField(
        _("Data Source Quotations"),
        default=dict,
        validators=[SchemaValidator(schema.QuotationsSchema)],
    )

    """ calculated properties """
    name_unknown = models.BooleanField(default=False)
    involvements_snapshot = models.JSONField(blank=True, default=list)

    def __str__(self):
        return f"{self.name} (#{self.id})"

    def is_current_draft(self):
        return self.investor.draft_version_id == self.id

    def save(self, *args, **kwargs):
        self._recalculate_fields()
        super().save(*args, **kwargs)

    def _recalculate_fields(self):
        self.name_unknown = bool(
            re.search(r"(unknown|unnamed)", self.name, re.IGNORECASE)
        )

    def change_status(
        self,
        transition: VersionTransition,
        user: User,
        to_user_id: int = None,
        comment="",
    ):
        old_draft_status = self.status

        super().change_status(transition=transition, user=user, to_user_id=to_user_id)

        if transition == VersionTransition.ACTIVATE:
            investor = self.investor
            investor.draft_version = None
            investor.active_version = self

            self._apply_snapshot()

            # recreate snapshot
            self.involvements_snapshot = self._create_snapshot()
            self.save()

            # recalculate depended fields
            investor.save()

            # close unresolved workflowinfos
            self.workflowinfos.all().update(resolved=True)

        elif transition == VersionTransition.TO_DRAFT:
            investor = self.investor
            investor.draft_version = self
            investor.save()

            # close remaining open feedback requests
            self.workflowinfos.filter(
                Q(
                    status_before__in=[
                        VersionStatus.REVIEW,
                        VersionStatus.ACTIVATION,
                    ]
                )
                & Q(status_after=VersionStatus.DRAFT)
                & (Q(from_user=user) | Q(to_user=user))
            ).update(resolved=True)

        # TODO: REfactor out

        InvestorWorkflowInfo.objects.create(
            investor_id=self.investor_id,
            investor_version=self,
            from_user=user,
            to_user_id=to_user_id,
            status_before=old_draft_status,
            status_after=self.status,
            comment=comment,
        )

    def _apply_snapshot(self):
        existing_ids = Involvement.objects.filter(
            id__in=[invo["id"] for invo in self.involvements_snapshot if invo["id"]]
        ).values_list("id", flat=True)

        Involvement.objects.filter(child_investor=self.investor).exclude(
            id__in=existing_ids
        ).delete()

        for invo in self.involvements_snapshot:
            try:
                i1 = Involvement.objects.get(id=invo["id"])
            except Involvement.DoesNotExist:
                i1 = Involvement(child_investor=self.investor)

            i1.nid = invo["nid"]
            i1.parent_investor_id = invo["parent_investor_id"]
            i1.role = invo["role"]
            i1.investment_type = invo["investment_type"]
            i1.percentage = invo["percentage"]
            i1.loans_amount = invo["loans_amount"]
            i1.loans_currency_id = invo["loans_currency_id"]
            i1.loans_date = invo["loans_date"]
            i1.parent_relation = invo["parent_relation"]
            i1.comment = invo["comment"]
            i1.save()

    def _create_snapshot(self) -> list[dict]:
        from apps.landmatrix.serializers import InvolvementSerializer

        return InvolvementSerializer(self.investor.get_parents(), many=True).data

    def copy_to_new_draft(self, created_by_id: int):
        old_self = InvestorVersion.objects.get(pk=self.pk)

        super().copy_to_new_draft(created_by_id)
        self.save()

        for d1 in old_self.datasources.all():
            d1.id = None
            d1.investorversion = self
            d1.save()


class InvestorDataSource(BaseDataSource):
    investorversion = models.ForeignKey(
        InvestorVersion,
        on_delete=models.CASCADE,
        related_name="datasources",
    )

    class Meta:
        unique_together = ["investorversion", "nid"]
        indexes = [models.Index(fields=["investorversion", "nid"])]
        ordering = ["id"]


class InvestorWorkflowInfo(BaseWorkflowInfo):
    investor = models.ForeignKey(
        InvestorHull,
        on_delete=models.CASCADE,
        related_name="workflowinfos",
    )
    investor_version = models.ForeignKey(
        InvestorVersion,
        on_delete=models.SET_NULL,
        related_name="workflowinfos",
        null=True,
        blank=True,
    )

    def get_object_url(self):
        base_url = super().get_object_url()
        return base_url + f"/investor/{self.investor_id}/"
