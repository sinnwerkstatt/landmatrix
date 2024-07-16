from django.db import models
from django.contrib.postgres.fields import ArrayField

from django.conf import settings
from django.utils import timezone
from datetime import datetime

from django.utils.translation import gettext as _

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
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=1000)
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        blank=True,
        null=True,
        on_delete=models.PROTECT,
        related_name="owned_projects",
    )
    editors = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        blank=True,
        null=True,
        on_delete=models.PROTECT,
        related_name="editable_projects",
    )
    created_at = models.DateTimeField(_("Created at"), default=timezone.now)
    modified_at = models.DateTimeField(_("Modified at"), default=timezone.now)
    modified_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        blank=True,
        null=True,
        on_delete=models.PROTECT,
        related_name="+",
    )
    filters = models.JSONField()