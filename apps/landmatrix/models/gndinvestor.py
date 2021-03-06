import re
from typing import Set

from django.contrib.postgres.fields import ArrayField
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

from apps.landmatrix.models import Country, Currency
from apps.landmatrix.models.versions import Version, register_version


class InvestorQuerySet(models.QuerySet):
    def active(self):
        return self.filter(status__in=(2, 3))

    # at the moment the only thing we filter on is the "status".
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
    def to_dict(self, use_object=False):
        investor = self.retrieve_object() if use_object else self.fields
        return {
            "id": self.id,
            "investor": investor,
            "revision": self.revision,
            "object_id": self.object_id,
        }


@register_version(InvestorVersion)
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

    involvements = models.ManyToManyField(
        "self",
        through="InvestorVentureInvolvement",
        through_fields=("venture", "investor"),
        symmetrical=False,
    )

    STATUS_DRAFT = 1
    STATUS_LIVE = 2
    STATUS_UPDATED = 3
    STATUS_DELETED = 4
    STATUS_CHOICES = (
        (STATUS_DRAFT, _("Draft")),
        (STATUS_LIVE, _("Live")),
        (STATUS_UPDATED, _("Updated")),
        (STATUS_DELETED, _("Deleted")),
    )
    DRAFT_STATUS_DRAFT = 1
    DRAFT_STATUS_REVIEW = 2
    DRAFT_STATUS_ACTIVATION = 3
    DRAFT_STATUS_REJECTED = 4
    DRAFT_STATUS_TO_DELETE = 5
    DRAFT_STATUS_CHOICES = (
        (DRAFT_STATUS_DRAFT, _("Draft")),
        (DRAFT_STATUS_REVIEW, _("Review")),
        (DRAFT_STATUS_ACTIVATION, _("Activation")),
        (DRAFT_STATUS_REJECTED, _("Rejected")),
        (DRAFT_STATUS_TO_DELETE, _("To Delete")),
    )
    status = models.IntegerField(choices=STATUS_CHOICES, default=1)
    draft_status = models.IntegerField(
        choices=DRAFT_STATUS_CHOICES, null=True, blank=True
    )
    created_at = models.DateTimeField(_("Created"), default=timezone.now)
    modified_at = models.DateTimeField(_("Last update"), blank=True, null=True)

    old_id = models.IntegerField(null=True, blank=True)

    objects = InvestorQuerySet.as_manager()

    """ # computed properties """
    # The following flag is needed at the moment to filter through Deals (public-filter)
    # FIXME This should be replaced by an option to _NOT_ specify the investor name.
    is_actually_unknown = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        self.is_actually_unknown = bool(
            re.search(r"(unknown|unnamed)", self.name, re.IGNORECASE)
        )
        super().save(*args, **kwargs)

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


class InvestorVentureInvolvementVersion(Version):
    pass


@register_version(InvestorVentureInvolvementVersion)
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
    loans_date = models.CharField(_("Loan date"), max_length=20, blank=True)

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
    comment = models.TextField(_("Comment"), blank=True)

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
