from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

from apps.landmatrix.models.activity import Activity, HistoricalActivity
from apps.landmatrix.models.activity_attribute_group import (
    ActivityAttribute,
    ActivityAttributeGroup,
    HistoricalActivityAttribute,
)
from apps.landmatrix.models.activity_changeset import ActivityChangeset, ReviewDecision
from apps.landmatrix.models.activity_feedback import ActivityFeedback
from apps.landmatrix.models.country import Country, Region
from apps.landmatrix.models.filter import (
    FilterCondition,
    FilterPreset,
    FilterPresetGroup,
)
from apps.landmatrix.models.investor import (
    HistoricalInvestor,
    HistoricalInvestorActivityInvolvement,
    HistoricalInvestorVentureInvolvement,
    Investor,
    InvestorActivityInvolvement,
    InvestorBase,
    InvestorVentureInvolvement,
)


class AgriculturalProduce(models.Model):
    name = models.CharField("Name", max_length=255)

    def __str__(self):
        return self.name


class Animal(models.Model):
    code = models.CharField("Code", max_length=255)
    name = models.CharField("Name", max_length=255)

    def __str__(self):
        return self.name


class Comment(models.Model):
    id = models.AutoField(primary_key=True)
    comment = models.TextField(_("Comment"))
    timestamp = models.DateTimeField(_("Timestamp"), default=timezone.now)
    fk_user = models.ForeignKey(
        User, verbose_name=_("User"), blank=True, null=True, on_delete=models.SET_NULL
    )
    fk_activity = models.ForeignKey(
        "Activity",
        verbose_name=_("Activity"),
        blank=True,
        null=True,
        on_delete=models.CASCADE,
    )
    fk_activity_attribute_group = models.ForeignKey(
        "ActivityAttributeGroup",
        verbose_name=_("Activity attribute group"),
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
    )

    def __str__(self):
        return self.comment


class Crop(models.Model):
    fk_agricultural_produce = models.ForeignKey(
        "AgriculturalProduce",
        null=True,
        verbose_name=_("Agricultural produce"),
        on_delete=models.SET_NULL,
    )
    code = models.CharField("Code", max_length=255)
    name = models.CharField("Name", max_length=255)
    slug = models.SlugField("Slug")

    def __str__(self):
        return self.name


class Currency(models.Model):
    code = models.CharField("Code", max_length=3)
    name = models.CharField("Name", max_length=255)
    symbol = models.CharField("Symbol", max_length=255)
    country = models.CharField("Country", max_length=2)
    ranking = models.IntegerField("Ranking")

    def __str__(self):
        return str("%s%s" % (self.name, self.symbol and " (%s)" % self.symbol or ""))


class Language(models.Model):
    english_name = models.CharField(_("English name"), max_length=255)
    local_name = models.CharField(_("Local name"), max_length=255)
    locale = models.CharField(_("Locale"), max_length=31)


class Mineral(models.Model):
    code = models.CharField("Code", max_length=255)
    name = models.CharField("Name", max_length=255)

    def __str__(self):
        return self.name


class Status(models.Model):
    name = models.CharField(_("Name"), max_length=255, db_index=True)
    description = models.TextField(_("Description"), blank=True, null=True)

    def __str__(self):
        return f"{self.id}: {self.name}"
