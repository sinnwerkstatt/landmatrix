import re
from typing import Set

from django.conf import settings
from django.contrib.postgres.fields import ArrayField
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from apps.landmatrix.models import Country, Currency
from apps.landmatrix.models.abstracts import (
    STATUS_CHOICES,
    DRAFT_STATUS_CHOICES,
    Version,
    WorkflowInfo,
)

from apps.utils import ecma262


class InvestorQuerySet(models.QuerySet):
    def active(self):
        return self.filter(status__in=(2, 3))

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
        return self


class InvestorVersion(Version):
    object = models.ForeignKey(
        "Investor",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="versions",
    )

    def enriched_dict(self) -> dict:
        edict = super().enriched_dict()
        if edict.get("investors"):
            imap = {
                i["id"]: i
                for i in Investor.objects.filter(
                    id__in=[ivs["investor"] for ivs in edict["investors"]]
                ).values("id", "name", "country_id")
            }
            for inv in edict["investors"]:
                iid = inv["investor"]
                inv["investor"] = {
                    "id": iid,
                    "name": imap[iid]["name"],
                    "country": {"id": imap[iid]["country_id"]},
                }
        return edict

    def to_dict(self):
        self.serialized_data["id"] = self.object_id
        return {
            "id": self.id,
            "object_id": self.object_id,
            "created_at": self.created_at,
            "created_by": self.created_by,
            "investor": self.serialized_data,
        }


class Investor(models.Model):
    name = models.CharField(_("Name"), max_length=1024)
    country = models.ForeignKey(
        Country,
        verbose_name=_("Country of registration/origin"),
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
    )

    CLASSIFICATION_CHOICES = (
        ("GOVERNMENT", _("Government")),
        ("GOVERNMENT_INSTITUTION", _("Government institution")),
        ("STATE_OWNED_COMPANY", _("State-/government (owned) company")),
        ("SEMI_STATE_OWNED_COMPANY", _("Semi state-owned company")),
        ("ASSET_MANAGEMENT_FIRM", _("Asset management firm")),
        (
            "BILATERAL_DEVELOPMENT_BANK",
            _("Bilateral Development Bank / Development Finance Institution"),
        ),
        ("STOCK_EXCHANGE_LISTED_COMPANY", _("Stock-exchange listed company")),
        ("COMMERCIAL_BANK", _("Commercial Bank")),
        ("INSURANCE_FIRM", _("Insurance firm")),
        ("INVESTMENT_BANK", _("Investment Bank")),
        ("INVESTMENT_FUND", _("Investment fund")),
        ("MULTILATERAL_DEVELOPMENT_BANK", _("Multilateral Development Bank (MDB)")),
        ("PRIVATE_COMPANY", _("Private company")),
        ("PRIVATE_EQUITY_FIRM", _("Private equity firm")),
        ("INDIVIDUAL_ENTREPRENEUR", _("Individual entrepreneur")),
        ("NON_PROFIT", _("Non - Profit organization (e.g. Church, University etc.)")),
        ("OTHER", _("Other (please specify in comment field)")),
    )
    classification = models.CharField(
        verbose_name=_("Classification"),
        max_length=100,
        choices=CLASSIFICATION_CHOICES,
        blank=True,
        null=True,
    )

    homepage = models.URLField(_("Investor homepage"), blank=True)
    opencorporates = models.URLField(
        _("Opencorporates link"), blank=True
    )  # opencorporates_link

    comment = models.TextField(_("Comment"), blank=True)

    # NOTE maybe toss this out; seems to confuse more.
    involvements = models.ManyToManyField(
        "self",
        through="InvestorVentureInvolvement",
        through_fields=("venture", "investor"),
        symmetrical=False,
    )

    status = models.IntegerField(choices=STATUS_CHOICES, default=1)
    draft_status = models.IntegerField(
        choices=DRAFT_STATUS_CHOICES, null=True, blank=True
    )
    current_draft = models.ForeignKey(
        InvestorVersion, null=True, blank=True, on_delete=models.SET_NULL
    )

    created_at = models.DateTimeField(_("Created"), default=timezone.now)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )
    modified_at = models.DateTimeField(_("Last update"), blank=True, null=True)
    modified_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )

    old_id = models.IntegerField(null=True, blank=True)

    objects = InvestorQuerySet.as_manager()

    """ # computed properties """
    # The following flag is needed at the moment to filter through Deals (public-filter)
    # NOTE This should be replaced by an option to _NOT_ specify the investor name.
    is_actually_unknown = models.BooleanField(default=False)

    def recalculate_fields(self):
        self.is_actually_unknown = bool(
            re.search(r"(unknown|unnamed)", self.name, re.IGNORECASE)
        )

    def save(self, *args, **kwargs):
        self.recalculate_fields()
        super().save(*args, **kwargs)

    def serialize_for_version(self) -> dict:
        investors = self._investors if hasattr(self, "_investors") else []

        return {
            "name": self.name,
            "country": self.country_id,
            "classification": self.classification,
            "homepage": self.homepage,
            "opencorporates": self.opencorporates,
            "comment": self.comment,
            "investors": [ivi.serialize() for ivi in investors],
            "status": self.status,
            "draft_status": self.draft_status,
            "created_at": ecma262(self.created_at),
            "created_by": self.created_by_id,
            "modified_at": ecma262(self.modified_at),
            "modified_by": self.modified_by_id,
            "is_actually_unknown": self.is_actually_unknown,
        }

    @classmethod
    def deserialize_from_version(cls, version: InvestorVersion):
        inv = cls(
            id=version.object_id,
            name=version.serialized_data["name"],
            country_id=version.serialized_data["country"],
            classification=version.serialized_data["classification"],
            homepage=version.serialized_data["homepage"],
            opencorporates=version.serialized_data["opencorporates"],
            comment=version.serialized_data["comment"],
            status=version.serialized_data["status"],
            draft_status=version.serialized_data["draft_status"],
            created_at=version.serialized_data["created_at"],
            created_by_id=version.serialized_data["created_by"],
            modified_at=version.serialized_data["modified_at"],
            modified_by_id=version.serialized_data["modified_by"],
            is_actually_unknown=version.serialized_data["is_actually_unknown"],
        )
        inv.save()

        current_invs = set(
            InvestorVentureInvolvement.objects.filter(venture_id=inv.id).values_list(
                "id", flat=True
            )
        )
        for ivi in version.serialized_data["investors"]:
            ix, created = InvestorVentureInvolvement.objects.get_or_create(
                id=ivi["id"],
                investor_id=ivi["investor"],
                venture_id=ivi["venture"],
            )
            ix.role = ivi["role"]
            ix.investment_type = ivi["investment_type"]
            ix.percentage = ivi["percentage"]
            ix.loans_amount = ivi["loans_amount"]
            ix.loans_currency = ivi["loans_currency"]
            ix.loans_date = ivi["loans_date"]
            ix.parent_relation = ivi["parent_relation"]
            ix.comment = ivi["comment"]
            ix.save()
            current_invs.discard(ix.id)

        InvestorVentureInvolvement.objects.filter(id__in=current_invs).delete()
        return inv

    def __str__(self):
        if self.name:
            return f"{self.name} (#{self.id})"
        return f"s#{self.id}"

    def get_parent_companies(
        self, top_investors_only=False, _seen_investors=None
    ) -> Set["Investor"]:
        """
        Get list of highest parent companies
        (all right-hand side parent companies of the network visualisation)
        """
        if _seen_investors is None:
            _seen_investors = {self}

        investor_involvements = (
            self.investors.active()
            .filter(role="PARENT")
            .exclude(investor__in=_seen_investors)
        )

        self.is_top_investor = not investor_involvements

        for involvement in investor_involvements:
            if involvement.investor in _seen_investors:
                continue
            _seen_investors.add(involvement.investor)
            involvement.investor.get_parent_companies(
                top_investors_only, _seen_investors
            )
        return _seen_investors

    def get_affected_deals(self, seen_investors=None):
        """
        Get list of affected deals - this is like Top Investors, only downwards
        (all left-hand side deals of the network visualisation)
        """
        deals = set()
        if seen_investors is None:
            seen_investors = {self}

        investor_ventures = (
            self.ventures.active()
            .filter(role="PARENT")
            .exclude(venture__in=seen_investors)
        )

        for deal in self.deals.all():
            deals.add(deal)

        # if not investor_involvements:
        #     investors.add(self)
        for involvements in investor_ventures:
            if involvements.venture in seen_investors:
                continue
            seen_investors.add(involvements.venture)
            deals.update(involvements.venture.get_affected_deals(seen_investors))
        return deals

    # TODO This is not working yet.
    def update_from_dict(self, payload: dict):
        for key, value in payload.items():
            if key in [
                "id",
                "created_at",
                "modified_at",
                "versions",
                "comments",
                "status",
                "draft_status",
                "workflowinfos",
                "__typename",
            ]:
                continue  # ignore these fields
            elif key in [
                x.name
                for x in self._meta.fields
                if x.__class__.__name__ == "ForeignKey"
            ]:
                self.__setattr__(f"{key}_id", value["id"] if value else None)
            elif key == "investors":
                _ivis = []
                for entry in value:
                    _ivi = InvestorVentureInvolvement()
                    if entry.get("id"):
                        _ivi.id = entry["id"]
                    _ivi.venture_id = self.id
                    _ivi.investor_id = entry["investor"]["id"]
                    _ivi.role = entry["role"]
                    _ivi.investment_type = entry.get("investment_type")
                    _ivi.percentage = entry.get("percentage")
                    _ivi.loans_amount = entry.get("loans_amount")
                    _ivi.loans_currency_id = (
                        entry["loans_currency"]["id"]
                        if entry.get("loans_currency")
                        else None
                    )
                    _ivi.loans_date = entry.get("loans_date", "")
                    _ivi.parent_relation = entry.get("parent_relation")
                    _ivi.comment = entry.get("comment", "")
                    _ivis += [_ivi]
                self._investors = _ivis
            else:
                self.__setattr__(key, value)

    def to_dict(self):
        country = (
            {"name": self.country.name, "code": self.country.code_alpha2}
            if self.country
            else None
        )
        return {
            "id": self.id,
            "name": self.name,
            "country": country,
            "classification": self.classification,
            "homepage": self.homepage,
            "opencorporates": self.opencorporates,
            "comment": self.comment,
            "status": self.status,
            "draft_status": self.draft_status,
            "deals": list(
                self.deals.public().values(
                    "id",
                    "recognition_status",
                    "country__name",
                    "nature_of_deal",
                    "intention_of_investment",
                    "intended_size",
                    "contract_size",
                    "negotiation_status",
                    "implementation_status",
                    "deal_size",
                )
            ),
        }


class InvestorWorkflowInfo(WorkflowInfo):
    investor = models.ForeignKey(
        Investor, on_delete=models.CASCADE, related_name="workflowinfos"
    )
    investor_version = models.ForeignKey(
        InvestorVersion,
        on_delete=models.SET_NULL,
        related_name="workflowinfos",
        null=True,
        blank=True,
    )

    def to_dict(self) -> dict:
        d = super().to_dict()
        d.update({"investor": self.investor, "investor_version": self.investor_version})
        return d


class InvestorVentureInvolvementQuerySet(models.QuerySet):
    def active(self):
        return self.filter(investor__status__in=(2, 3), venture__status__in=(2, 3))

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


class InvestorVentureInvolvement(models.Model):
    investor = models.ForeignKey(
        Investor,
        verbose_name=_("Investor"),
        db_index=True,
        related_name="ventures",
        on_delete=models.PROTECT,
    )
    venture = models.ForeignKey(
        Investor,
        verbose_name=_("Venture Company"),
        db_index=True,
        related_name="investors",
        on_delete=models.PROTECT,
    )

    ROLE_CHOICES = (
        ("PARENT", _("Parent company")),
        ("LENDER", _("Tertiary investor/lender")),
    )
    role = models.CharField(
        verbose_name=_("Relation type"), max_length=100, choices=ROLE_CHOICES
    )

    INVESTMENT_TYPE_CHOICES = (
        ("EQUITY", _("Shares/Equity")),
        ("DEBT_FINANCING", _("Debt financing")),
    )
    investment_type = ArrayField(
        models.CharField(_("Investment type"), max_length=100),
        choices=INVESTMENT_TYPE_CHOICES,
        blank=True,
        null=True,
    )

    percentage = models.FloatField(
        _("Ownership share"),
        blank=True,
        null=True,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
    )
    loans_amount = models.FloatField(_("Loan amount"), blank=True, null=True)
    loans_currency = models.ForeignKey(
        Currency,
        verbose_name=_("Loan currency"),
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
    )
    loans_date = models.CharField(_("Loan date"), max_length=20, blank=True, default="")

    PARENT_RELATION_CHOICES = (
        ("SUBSIDIARY", _("Subsidiary of parent company")),  # Subsidiary
        ("LOCAL_BRANCH", _("Local branch of parent company")),  # Local branch
        ("JOINT_VENTURE", _("Joint venture of parent companies")),  # Joint venture
    )
    parent_relation = models.CharField(
        verbose_name=_("Parent relation"),
        max_length=100,
        choices=PARENT_RELATION_CHOICES,
        blank=True,
        null=True,
    )
    comment = models.TextField(_("Comment"), blank=True, default="")

    old_id = models.IntegerField(null=True, blank=True)

    objects = InvestorVentureInvolvementQuerySet.as_manager()

    class Meta:
        verbose_name = _("Investor Venture Involvement")
        verbose_name_plural = _("Investor Venture Involvements")
        ordering = ["-id"]

    def __str__(self):
        if self.role == "PARENT":
            role = _("<is PARENT of>")
        else:
            role = _("<is INVESTOR of>")
        return f"{self.investor} {role} {self.venture}"

    def to_dict(self):
        return {
            "id": self.id,
            "role": self.role,
            "investment_type": self.investment_type,
            "percentage": self.percentage,
            "loans_amount": self.loans_amount,
            "loans_currency": self.loans_currency,
            "loans_date": self.loans_date,
            "parent_relation": self.parent_relation,
            "comment": self.comment,
        }

    def serialize(self) -> dict:
        return {
            "id": self.id,
            "investor": self.investor_id,
            "venture": self.venture_id,
            "role": self.role,
            "investment_type": self.investment_type,
            "percentage": self.percentage,
            "loans_amount": self.loans_amount,
            "loans_currency": self.loans_currency_id,
            "loans_date": self.loans_date,
            "parent_relation": self.parent_relation,
            "comment": self.comment,
        }
