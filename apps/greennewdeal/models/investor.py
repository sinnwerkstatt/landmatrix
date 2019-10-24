import reversion
from django.contrib.postgres.fields import ArrayField
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

from apps.greennewdeal.models.country import Country


@reversion.register(follow=["involvements"], ignore_duplicates=True)
class Investor(models.Model):
    name = models.CharField(_("Name"), max_length=1024)
    country = models.ForeignKey(
        Country,
        verbose_name=_("Country of registration/origin"),
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
    )  # fk_country

    STAKEHOLDER_CLASSIFICATIONS = (
        (10, _("Private company")),
        (20, _("Stock-exchange listed company")),
        (30, _("Individual entrepreneur")),
        (40, _("Investment fund")),
        (50, _("Semi state-owned company")),
        (60, _("State-/government (owned) company")),
        (70, _("Other (please specify in comment field)")),
    )
    INVESTOR_CLASSIFICATIONS = (
        (110, _("Government")),
        (120, _("Government institution")),
        (130, _("Multilateral Development Bank (MDB)")),
        (140, _("Bilateral Development Bank / Development Finance Institution")),
        (150, _("Commercial Bank")),
        (160, _("Investment Bank")),
        (
            170,
            _(
                "Investment Fund (all types incl. pension, hedge, mutual, private equity funds etc.)"
            ),
        ),
        (180, _("Insurance firm")),
        (190, _("Private equity firm")),
        (200, _("Asset management firm")),
        (210, _("Non - Profit organization (e.g. Church, University etc.)")),
    )
    CLASSIFICATION_CHOICES = STAKEHOLDER_CLASSIFICATIONS + INVESTOR_CLASSIFICATIONS
    classification = models.IntegerField(
        verbose_name=_("Classification"),
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

    STATUS_CHOICES = [
        (1, _("Draft")),
        (2, _("Live")),
        (3, _("Live + Draft")),
        (4, _("Deleted")),
        (5, _("Rejected")),
        (6, _("To Delete?")),
    ]
    status = models.IntegerField(choices=STATUS_CHOICES, default=1)
    timestamp = models.DateTimeField(default=timezone.now, null=False)

    def __str__(self):
        return f"{self.name} (#{self.id})"

    def save_revision(self, draft=False, date=None, user=None, comment=None):
        if draft:
            status = 3 if self.pk else 1
        else:
            status = 2

        with reversion.create_revision():
            self.status = status
            reversion.add_to_revision(self)
            reversion.set_date_created(date)
            reversion.set_user(user)
            reversion.set_comment(comment)

            if not draft:
                self.save()
        self.__class__.objects.filter(pk=self.pk).update(status=status)


@reversion.register(ignore_duplicates=True)
class InvestorVentureInvolvement(models.Model):
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

    STAKEHOLDER_ROLE = 10
    INVESTOR_ROLE = 20
    ROLE_CHOICES = (
        (STAKEHOLDER_ROLE, _("Parent company")),
        (INVESTOR_ROLE, _("Tertiary investor/lender")),
    )
    role = models.IntegerField(verbose_name=_("Relation type"), choices=ROLE_CHOICES)

    EQUITY_INVESTMENT_TYPE = 10
    DEBT_FINANCING_INVESTMENT_TYPE = 20
    INVESTMENT_TYPE_CHOICES = (
        (EQUITY_INVESTMENT_TYPE, _("Shares/Equity")),
        (DEBT_FINANCING_INVESTMENT_TYPE, _("Debt financing")),
    )
    investment_type = ArrayField(
        models.IntegerField(_("Investment type"), choices=INVESTMENT_TYPE_CHOICES),
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
        "Currency",
        verbose_name=_("Loan currency"),
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
    )
    loans_date = models.CharField(_("Loan date"), max_length=10, blank=True)

    PARENT_RELATION_CHOICES = (
        (10, _("Subsidiary of parent company")),  # Subsidiary
        (20, _("Local branch of parent company")),  # Local branch
        (30, _("Joint venture of parent companies")),  # Joint venture
    )
    parent_relation = models.IntegerField(
        verbose_name=_("Parent relation"),
        choices=PARENT_RELATION_CHOICES,
        blank=True,
        null=True,
    )
    comment = models.TextField(_("Comment"), blank=True)

    STATUS_CHOICES = [
        (1, _("Draft")),
        (2, _("Live")),
        (3, _("Live + Draft")),
        (4, _("Deleted")),
        (5, _("Rejected")),
        (6, _("To Delete?")),
    ]
    status = models.IntegerField(choices=STATUS_CHOICES, default=1)
    timestamp = models.DateTimeField(default=timezone.now, null=False)
    old_id = models.IntegerField(null=True, blank=True)

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

    def save_revision(self, draft=False, date=None, user=None, comment=None):
        if draft:
            status = 3 if self.pk else 1
        else:
            status = 2

        with reversion.create_revision():
            self.status = status
            reversion.add_to_revision(self)

            if not draft:
                self.save()
        self.__class__.objects.filter(pk=self.pk).update(status=status)
