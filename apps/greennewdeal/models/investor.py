import reversion
from django.contrib.postgres.fields import ArrayField
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

from apps.greennewdeal.models import Country, Currency
from apps.greennewdeal.models.mixins import (
    ReversionSaveMixin,
    UnderscoreDisplayParseMixin,
)


class InvestorManager(models.Manager):
    def visible(self, user=None):
        qs = self.get_queryset()
        if user and (user.is_staff or user.is_superuser):
            return qs
        return qs.filter(status__in=(2, 3))


@reversion.register(follow=["involvements"], ignore_duplicates=True)
class Investor(models.Model, UnderscoreDisplayParseMixin, ReversionSaveMixin):
    name = models.CharField(_("Name"), max_length=1024, blank=True, null=True)
    country = models.ForeignKey(
        Country,
        verbose_name=_("Country of registration/origin"),
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
    )

    STAKEHOLDER_CLASSIFICATIONS = (
        ("PRIVATE_COMPANY", _("Private company")),
        ("STOCK_EXCHANGE_LISTED_COMPANY", _("Stock-exchange listed company")),
        ("INDIVIDUAL_ENTREPRENEUR", _("Individual entrepreneur")),
        ("INVESTMENT_FUND", _("Investment fund")),
        ("SEMI_STATE_OWNED_COMPANY", _("Semi state-owned company")),
        ("STATE_OWNED_COMPANY", _("State-/government (owned) company")),
        ("OTHER", _("Other (please specify in comment field)")),
    )
    INVESTOR_CLASSIFICATIONS = (
        ("GOVERNMENT", _("Government")),
        ("GOVERNMENT_INSTITUTION", _("Government institution")),
        ("MULTILATERAL_DEVELOPMENT_BANK", _("Multilateral Development Bank (MDB)")),
        (
            "BILATERAL_DEVELOPMENT_BANK",
            _("Bilateral Development Bank / Development Finance Institution"),
        ),
        ("COMMERCIAL_BANK", _("Commercial Bank")),
        ("INVESTMENT_BANK", _("Investment Bank")),
        ("INSURANCE_FIRM", _("Insurance firm")),
        ("PRIVATE_EQUITY_FIRM", _("Private equity firm")),
        ("ASSET_MANAGEMENT_FIRM", _("Asset management firm")),
        ("NON_PROFIT", _("Non - Profit organization (e.g. Church, University etc.)")),
    )
    CLASSIFICATION_CHOICES = STAKEHOLDER_CLASSIFICATIONS + INVESTOR_CLASSIFICATIONS
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
        "self", through="InvestorVentureInvolvement", symmetrical=False,
    )

    STATUS_CHOICES = (
        (1, _("Draft")),
        (2, _("Live")),
        (3, _("Updated")),
        (4, _("Deleted")),
        (5, _("Rejected")),
        (6, _("To Delete?")),
    )
    DRAFT_STATUS_CHOICES = (
        (1, "Draft"),
        (2, "Review"),
        (3, "Activation"),
    )
    status = models.IntegerField(choices=STATUS_CHOICES, default=1)
    draft_status = models.IntegerField(
        choices=DRAFT_STATUS_CHOICES, null=True, blank=True
    )
    timestamp = models.DateTimeField(default=timezone.now, null=False)

    objects = InvestorManager()

    def __str__(self):
        return f"{self.name} (#{self.id})"

    def get_top_investors(self, seen_investors=None):
        """
        Get list of highest parent companies
        (all right-hand side parent companies of the network visualisation)
        """
        investors = set()
        if seen_investors is None:
            seen_investors = {self}

        investor_involvements = self.investors.filter(
            investor__status__in=[self.STATUS_LIVE, self.STATUS_LIVE_AND_DRAFT],
            venture__status__in=[self.STATUS_LIVE, self.STATUS_LIVE_AND_DRAFT],
            role=InvestorVentureInvolvement.STAKEHOLDER_ROLE,
        ).exclude(investor__in=seen_investors)

        if not investor_involvements:
            investors.add(self)
        for involvement in investor_involvements:
            if involvement.investor in seen_investors:
                continue
            seen_investors.add(involvement.investor)
            investors.update(involvement.investor.get_top_investors(seen_investors))
        return investors


class InvolvementManager(models.Manager):
    def visible(self, user=None):
        qs = self.get_queryset()
        if user and (user.is_staff or user.is_superuser):
            return qs
        return qs.filter(status__in=(2, 3))


@reversion.register(ignore_duplicates=True)
class InvestorVentureInvolvement(
    models.Model, UnderscoreDisplayParseMixin, ReversionSaveMixin
):
    investor = models.ForeignKey(
        Investor,
        verbose_name=_("Investor"),
        db_index=True,
        related_name="venture_involvements",
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
        ("STAKEHOLDER", _("Parent company")),
        ("INVESTOR", _("Tertiary investor/lender")),
    )
    role = models.CharField(
        verbose_name=_("Relation type"), max_length=100, choices=ROLE_CHOICES
    )

    INVESTMENT_TYPE_CHOICES = (
        ("EQUITY", _("Shares/Equity")),
        ("DEBT_FINANCING", _("Debt financing")),
    )
    investment_type = ArrayField(
        models.CharField(
            _("Investment type"), max_length=100, choices=INVESTMENT_TYPE_CHOICES
        ),
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

    STATUS_CHOICES = (
        (1, _("Draft")),
        (2, _("Live")),
        (3, _("Updated")),
        (4, _("Deleted")),
        (5, _("Rejected")),
        (6, _("To Delete?")),
    )
    DRAFT_STATUS_CHOICES = (
        (1, "Draft"),
        (2, "Review"),
        (3, "Activation"),
    )
    status = models.IntegerField(choices=STATUS_CHOICES, default=1)
    draft_status = models.IntegerField(
        choices=DRAFT_STATUS_CHOICES, null=True, blank=True
    )
    timestamp = models.DateTimeField(default=timezone.now, null=False)
    old_id = models.IntegerField(null=True, blank=True)

    objects = InvolvementManager()

    class Meta:
        verbose_name = _("Investor Venture Involvement")
        verbose_name_plural = _("Investor Venture Involvements")
        ordering = ["-id"]

    def __str__(self):
        if self.role == 10:
            role = _("<is PARENT of>")
        else:
            role = _("<is INVESTOR of>")
        return f"{self.investor} {role} {self.venture}"
