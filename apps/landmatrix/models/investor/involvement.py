from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.utils.translation import gettext as _

from apps.landmatrix.models import choices
from apps.landmatrix.models.currency import Currency
from apps.landmatrix.models.fields import ChoiceArrayField, LooseDateField
from apps.landmatrix.models.investor import InvestorHull


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
    # TODO: Add nanoId
    # nid = NanoIDField("ID", max_length=15, db_index=True, null=True)
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
        verbose_name=_("Relation type"), choices=choices.INVOLVEMENT_ROLE_CHOICES
    )

    investment_type = ChoiceArrayField(
        models.CharField(choices=choices.INVESTMENT_TYPE_CHOICES),
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
    loans_amount = models.FloatField(_("Loan amount"), blank=True, null=True)
    loans_currency = models.ForeignKey(
        Currency,
        verbose_name=_("Loan currency"),
        blank=True,
        null=True,
        on_delete=models.PROTECT,
    )
    loans_date = LooseDateField(_("Loan date"), blank=True, null=True)

    parent_relation = models.CharField(
        verbose_name=_("Parent relation"),
        choices=choices.PARENT_RELATION_CHOICES,
        blank=True,
        null=True,
    )
    comment = models.TextField(_("Comment"), blank=True)

    objects = InvolvementQuerySet.as_manager()

    class Meta:
        verbose_name = _("Investor Venture Involvement")
        verbose_name_plural = _("Investor Venture Involvements")
        ordering = ["id"]
        # would be nice to have but not today
        # maybe tomorrow?
        # unique_together = [["parent_investor", "child_investor"]]

    def __str__(self):
        if self.role == "PARENT":
            role = _("<is PARENT of>")
        else:
            role = _("<is INVESTOR of>")
        return f"{self.parent_investor} {role} {self.child_investor}"
