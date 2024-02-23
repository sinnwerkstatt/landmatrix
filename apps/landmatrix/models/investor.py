from __future__ import annotations

import re

from django.conf import settings
from django.contrib.postgres.fields import ArrayField
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from apps.utils import ecma262

from .abstracts import DRAFT_STATUS_CHOICES, STATUS_CHOICES, Version, WorkflowInfo
from .choices import INVESTOR_CLASSIFICATION_CHOICES
from .country import Country
from .currency import Currency
from .oldfields import DatasourcesField


class InvestorQuerySet(models.QuerySet):
    def active(self):
        return self.filter(status__in=(2, 3))

    def visible(self, user=None, subset="PUBLIC"):
        if subset in ["ACTIVE", "PUBLIC"]:
            return self.active()

        if not user or not user.is_authenticated:
            return self.active()

        return self


class InvestorVersion(Version):
    object = models.ForeignKey(
        "Investor",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="versions",
    )


class Investor(models.Model):
    name = models.CharField(_("Name"))
    country = models.ForeignKey(
        Country,
        verbose_name=_("Country of registration/origin"),
        blank=True,
        null=True,
        on_delete=models.PROTECT,
    )

    classification = models.CharField(
        verbose_name=_("Classification"),
        choices=INVESTOR_CLASSIFICATION_CHOICES,
        blank=True,
        null=True,
    )

    homepage = models.URLField(_("Investor homepage"), blank=True)
    opencorporates = models.URLField(
        _("Opencorporates link"), blank=True
    )  # opencorporates_link

    """ Data sources """
    datasources = DatasourcesField(_("Data sources"), default=list, blank=True)

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
        on_delete=models.PROTECT,
        related_name="+",
    )
    modified_at = models.DateTimeField(_("Last update"), blank=True, null=True)
    modified_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        blank=True,
        null=True,
        on_delete=models.PROTECT,
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

    def __str__(self):
        if self.name:
            return f"{self.name} (#{self.id})"
        return f"s#{self.id}"

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


class InvestorWorkflowInfoOld(WorkflowInfo):
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
    role = models.CharField(verbose_name=_("Relation type"), choices=ROLE_CHOICES)

    INVESTMENT_TYPE_CHOICES = (
        ("EQUITY", _("Shares/Equity")),
        ("DEBT_FINANCING", _("Debt financing")),
    )
    investment_type = ArrayField(
        models.CharField(choices=INVESTMENT_TYPE_CHOICES),
        verbose_name=_("Investment type"),
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
        on_delete=models.PROTECT,
    )
    loans_date = models.CharField(_("Loan date"), max_length=20, blank=True, default="")

    PARENT_RELATION_CHOICES = (
        ("SUBSIDIARY", _("Subsidiary of parent company")),  # Subsidiary
        ("LOCAL_BRANCH", _("Local branch of parent company")),  # Local branch
        ("JOINT_VENTURE", _("Joint venture of parent companies")),  # Joint venture
    )
    parent_relation = models.CharField(
        verbose_name=_("Parent relation"),
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
