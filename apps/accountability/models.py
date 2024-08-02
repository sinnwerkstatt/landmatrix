from django.db import models
from django.contrib.postgres.fields import ArrayField

from django.conf import settings
from django.utils import timezone
from datetime import datetime

from django.utils.translation import gettext as _

from apps.landmatrix.models import choices
from apps.landmatrix.models.new import DealHull

STATUS_CHOICES = [
    ("TO_SCORE", _("To score")),
    ("WAITING", _("Waiting")),
    ("VALIDATED", _("Validated")),
]

SCORE_CHOICES = [
    ("NO_SCORE", _("No score")),
    ("NO_DATA", _("Insufficient data")),
    ("NO_VIOLATIONS", _("No violation")),
    ("PARTIAL_VIOLATIONS", _("Violations")),
    ("SEVERE_VIOLATIONS", _("Severe violations")),
]

class UserInfo(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="info")
class VggtChapter(models.Model):
    chapter = models.PositiveIntegerField(primary_key=True)
    name = models.CharField(max_length=100)

    def __str__(self):
        return str(self.chapter)

class VggtArticle(models.Model):
    chapter = models.ForeignKey(VggtChapter, on_delete=models.CASCADE)
    article = models.PositiveIntegerField()
    description = models.CharField(max_length=2000)

    def __str__(self):
        return f"{self.chapter.name} - {self.article}"

class VggtVariable(models.Model):
    number = models.PositiveIntegerField()
    name = models.CharField(max_length=200)
    landmatrix_fields = ArrayField(models.CharField(max_length=100), size=50, blank=True, null=True)
    landmatrix_additional_fields = ArrayField(models.CharField(max_length=100), size=50, blank=True, null=True)
    scoring_help = ArrayField(models.CharField(max_length=2000), size=20, blank=True, null=True)

    def __str__(self):
        return f"{self.number} - {self.name}"

class DealScore(models.Model):
    test = models.CharField(max_length=30)
    deal = models.OneToOneField(DealHull, on_delete=models.CASCADE, primary_key=True)

    def __str__(self):
        return f"Score for deal {self.deal}"
    
    class Meta:
        ordering = ["deal"]

class DealVariable(models.Model):
    deal_score = models.ForeignKey(DealScore, on_delete=models.CASCADE)
    vggt_variable = models.ForeignKey(VggtVariable, on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)
    score = models.CharField(max_length=20, choices=SCORE_CHOICES)
    scored_at = models.DateTimeField(_("Created at"), null=True, blank=True)
    score_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        blank=True,
        null=True,
        on_delete=models.PROTECT,
        related_name="+",
    )
    assignee = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        blank=True,
        null=True,
        on_delete=models.PROTECT,
        related_name="todo",
    )

    def __str__(self):
        return f"{self.deal_score.deal} - {self.vggt_variable}"
    
    class Meta:
        ordering = ["deal_score", "vggt_variable"]
        unique_together = ["deal_score", "vggt_variable"]


class Project(models.Model):
    name = models.CharField(max_length=200, unique=True)
    description = models.CharField(max_length=1000)
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        blank=True,
        null=True,
        on_delete=models.PROTECT,
        related_name="owned_projects",
    )
    editors = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        blank=True,
        related_name="editable_projects",
    )
    created_at = models.DateTimeField(_("Created at"), default=timezone.now)
    modified_at = models.DateTimeField(_("Modified at"), blank=True, null=True)
    modified_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        blank=True,
        null=True,
        on_delete=models.PROTECT,
        related_name="+",
    )

    def __str__(self):
        return f"{self.name}"


class Filters(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="filters")
    region_id = ArrayField(models.PositiveIntegerField(), blank=True, null=True)
    country_id = ArrayField(models.PositiveIntegerField(), blank=True, null=True)
    area_min = models.PositiveIntegerField(blank=True, null=True)
    area_max = models.PositiveIntegerField(blank=True, null=True)
    negotiation_status = ArrayField(models.CharField(choices=choices.NEGOTIATION_STATUS_CHOICES), blank=True, null=True)
    nature_of_deal = ArrayField(models.CharField(choices=choices.NATURE_OF_DEAL_CHOICES), blank = True, null=True)
    investor_id = ArrayField(models.PositiveIntegerField(), blank=True, null=True)
    investor_country_id = ArrayField(models.PositiveIntegerField(), blank=True, null=True)
    initiation_year_min = models.PositiveIntegerField(blank=True, null=True)
    initiation_year_max = models.PositiveIntegerField(blank=True, null=True)
    initiation_year_unknown = models.BooleanField(default=True)
    implementation_status = ArrayField(models.CharField(choices=choices.IMPLEMENTATION_STATUS_CHOICES), blank=True, null=True)
    intention_of_investment = ArrayField(models.CharField(choices=choices.INTENTION_OF_INVESTMENT_CHOICES), blank=True, null=True)
    intention_of_investment_unknown = models.BooleanField(default=False)
    crops = ArrayField(models.CharField(choices=choices.CROPS_CHOICES), blank=True, null=True)
    animals = ArrayField(models.CharField(choices=choices.ANIMALS_CHOICES), blank=True, null=True)
    minerals = ArrayField(models.CharField(choices=choices.MINERALS_CHOICES), blank=True, null=True)
    transnational = models.BooleanField(blank=True, null=True)
    forest_concession = models.BooleanField(blank=True, null=True)

    def __str__(self):
        return f"{self.project.name} - filters"


class Bookmark(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="bookmarks")
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    order = models.PositiveIntegerField(blank=True, null=True)
    class Meta:
        unique_together=[["user", "project"]]