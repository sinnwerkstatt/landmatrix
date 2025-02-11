from django.conf import settings
from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext as _

from apps.landmatrix.models import choices
from apps.landmatrix.models.deal import DealHull, DealVersion
from apps.landmatrix.models.fields import ChoiceArrayField

STATUS_CHOICES = [
    ("TO_SCORE", _("To score")),
    ("WAITING", _("Waiting")),
    ("VALIDATED", _("Validated")),
]

NO_DATA = "NO_DATA"
SEVERE_VIOLATIONS = "SEVERE_VIOLATIONS"
PARTIAL_VIOLATIONS = "PARTIAL_VIOLATIONS"
NO_VIOLATIONS = "NO_VIOLATIONS"

SCORE_OPTIONS_CHOICES = [
    (NO_DATA, _("Insufficient data")),
    (SEVERE_VIOLATIONS, _("Severe violations")),
    (PARTIAL_VIOLATIONS, _("Violations")),
    (NO_VIOLATIONS, _("No violation")),
]


def get_default_score_options() -> list[str]:
    return [
        NO_DATA,
        SEVERE_VIOLATIONS,
        PARTIAL_VIOLATIONS,
        NO_VIOLATIONS,
    ]


SCORE_CHOICES = [("NO_SCORE", _("No score"))] + SCORE_OPTIONS_CHOICES


class UserInfo(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="info"
    )

    def __str__(self):
        return f"UserInfo {self.user.username}"


class VggtChapter(models.Model):
    chapter = models.PositiveIntegerField(primary_key=True)
    name = models.CharField(max_length=100)

    def __str__(self):
        return str(self.chapter)


class VggtArticle(models.Model):
    chapter = models.ForeignKey(VggtChapter, on_delete=models.CASCADE)
    article = models.PositiveIntegerField()
    description = models.CharField(max_length=2000)

    class Meta:
        unique_together = [["chapter", "article"]]

    def __str__(self):
        return f"{self.chapter.name} - {self.article}"


class VggtVariable(models.Model):
    number = models.PositiveIntegerField(primary_key=True)
    name = models.CharField(max_length=200)
    score_options = ChoiceArrayField(
        models.CharField(choices=SCORE_OPTIONS_CHOICES),
        blank=True,
        default=get_default_score_options,
    )
    landmatrix_fields = ArrayField(
        models.CharField(max_length=100), size=50, blank=True, null=True
    )
    landmatrix_additional_fields = ArrayField(
        models.CharField(max_length=100), size=50, blank=True, null=True
    )
    articles = models.ManyToManyField(VggtArticle, related_name="variables")

    class Meta:
        ordering = ["number"]

    def __str__(self):
        return f"{self.number} - {self.name}"


class DealScore(models.Model):
    deal = models.OneToOneField(
        DealHull,
        on_delete=models.CASCADE,
        primary_key=True,
        related_name="accountability_score_hull",
    )

    def __str__(self):
        return f"Score of deal {self.deal}"

    def current_score(self):
        try:
            return self.deal.active_version.accountability_score
        except:  # noqa: E722
            return None


class DealScoreVersion(models.Model):
    deal_version = models.OneToOneField(
        DealVersion,
        on_delete=models.CASCADE,
        primary_key=True,
        related_name="accountability_score",
    )
    score = models.ForeignKey(
        DealScore, on_delete=models.CASCADE, related_name="scores"
    )
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="TO_SCORE")

    def __str__(self):
        return f"Score of deal {self.score.deal} - Version {self.deal_version}"

    def save(self, *args, **kwargs):
        # On create, create related objects
        if self._state.adding:
            current_score = self.score.current_score()
            super(DealScoreVersion, self).save(*args, **kwargs)  # noqa: UP008

            # If variables already existed, copy content to the new variables, else create from scratch
            if current_score is not None:
                current_variables = DealVariable.objects.filter(
                    deal_score=current_score
                )
                for current_variable in current_variables:
                    status = (
                        "TO_SCORE"
                        if current_variable.status == "TO_SCORE"
                        else "WAITING"
                    )
                    variable = DealVariable(
                        deal_score=self,
                        vggt_variable=current_variable.vggt_variable,
                        status=status,
                        score=current_variable.score,
                        scored_at=current_variable.scored_at,
                        scored_by=current_variable.scored_by,
                        assignee=current_variable.assignee,
                    )
                    variable.save()
            else:
                vggt_variables = VggtVariable.objects.all()
                for vggt_variable in vggt_variables:
                    variable = DealVariable(
                        deal_score=self, vggt_variable=vggt_variable
                    )
                    variable.save()
        else:
            super().save(*args, **kwargs)

    def is_current(self):
        return True if self.score.current_score() else False


class DealVariable(models.Model):
    deal_score = models.ForeignKey(
        DealScoreVersion, on_delete=models.CASCADE, related_name="variables"
    )
    vggt_variable = models.ForeignKey(
        VggtVariable, on_delete=models.CASCADE, related_name="+"
    )
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="TO_SCORE")
    score = models.CharField(max_length=20, choices=SCORE_CHOICES, default="NO_SCORE")
    scored_at = models.DateTimeField(_("Scored at"), null=True, blank=True)
    scored_by = models.ForeignKey(
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

    class Meta:
        ordering = ["deal_score", "vggt_variable"]
        unique_together = ["deal_score", "vggt_variable"]

    def __str__(self):
        return f"Deal {self.deal_score.score.deal} - Variable {self.vggt_variable.number} (pk={self.pk})"

    def is_current(self):
        current_score = self.deal_score.score.current_score()
        return True if self.deal_score == current_score else False


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
    project = models.OneToOneField(
        Project, on_delete=models.CASCADE, related_name="filters"
    )
    region_id = ArrayField(models.PositiveIntegerField(), blank=True, null=True)
    country_id = ArrayField(models.PositiveIntegerField(), blank=True, null=True)
    area_min = models.PositiveIntegerField(blank=True, null=True)
    area_max = models.PositiveIntegerField(blank=True, null=True)
    negotiation_status = ArrayField(
        models.CharField(choices=choices.NEGOTIATION_STATUS_CHOICES),
        blank=True,
        null=True,
    )
    nature_of_deal = ArrayField(
        models.CharField(choices=choices.NATURE_OF_DEAL_CHOICES), blank=True, null=True
    )
    investor_id = ArrayField(models.PositiveIntegerField(), blank=True, null=True)
    investor_country_id = ArrayField(
        models.PositiveIntegerField(), blank=True, null=True
    )
    initiation_year_min = models.PositiveIntegerField(blank=True, null=True)
    initiation_year_max = models.PositiveIntegerField(blank=True, null=True)
    initiation_year_unknown = models.BooleanField(default=True)
    implementation_status = ArrayField(
        models.CharField(choices=choices.IMPLEMENTATION_STATUS_CHOICES),
        blank=True,
        null=True,
    )
    intention_of_investment = ArrayField(
        models.CharField(choices=choices.INTENTION_OF_INVESTMENT_CHOICES),
        blank=True,
        null=True,
    )
    intention_of_investment_unknown = models.BooleanField(default=False)
    crops = ArrayField(
        models.CharField(choices=choices.CROPS_CHOICES), blank=True, null=True
    )
    animals = ArrayField(
        models.CharField(choices=choices.ANIMALS_CHOICES), blank=True, null=True
    )
    minerals = ArrayField(
        models.CharField(choices=choices.MINERALS_CHOICES), blank=True, null=True
    )
    transnational = models.BooleanField(blank=True, null=True)
    forest_concession = models.BooleanField(blank=True, null=True)

    def __str__(self):
        return f"{self.project.name} - filters"


class Bookmark(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="bookmarks"
    )
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    order = models.PositiveIntegerField(blank=True, null=True)

    class Meta:
        unique_together = [["user", "project"]]

    def __str__(self):
        return f"Bookmark: {self.project.name}"
