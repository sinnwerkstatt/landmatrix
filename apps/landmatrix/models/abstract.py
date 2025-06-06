from nanoid import generate

from django.conf import settings
from django.db import models
from django.db.models import TextChoices
from django.utils import timezone
from django.utils.translation import gettext as _
from rest_framework.exceptions import ParseError, PermissionDenied
from wagtail.models import Site

from apps.accounts.models import User
from apps.landmatrix.models import choices, schema
from apps.landmatrix.models.fields import LooseDateField, NanoIDField
from apps.landmatrix.permissions import is_admin, is_editor_or_higher
from django_pydantic_jsonfield import PydanticJSONField, SchemaValidator


class BaseHull(models.Model):
    deleted = models.BooleanField(_("Deleted"), default=False)
    deleted_comment = models.TextField(_("Comment on deletion"), blank=True)

    # mainly for management/case_statistics
    first_created_at = models.DateTimeField(_("First created at"))
    first_created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name=_("First created by"),
        blank=True,
        null=True,
        on_delete=models.PROTECT,
        related_name="+",
    )

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        if self._state.adding and not self.first_created_at:
            self.first_created_at = timezone.now()
        super().save(*args, **kwargs)


class VersionStatus(TextChoices):
    DRAFT = "DRAFT", _("Draft")
    REVIEW = "REVIEW", _("Review")
    ACTIVATION = "ACTIVATION", _("Activation")
    ACTIVATED = "ACTIVATED", _("Activated")


class VersionTransition(TextChoices):
    TO_DRAFT = "TO_DRAFT"
    TO_REVIEW = "TO_REVIEW"
    TO_ACTIVATION = "TO_ACTIVATION"
    ACTIVATE = "ACTIVATE"


class BaseVersion(models.Model):
    created_at = models.DateTimeField(_("Created at"))
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name=_("Created by"),
        blank=True,
        null=True,
        on_delete=models.PROTECT,
        related_name="+",
    )
    modified_at = models.DateTimeField(
        _("Modified at"),
        blank=True,
        null=True,
    )
    modified_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name=_("Modified by"),
        blank=True,
        null=True,
        on_delete=models.PROTECT,
        related_name="+",
    )
    sent_to_review_at = models.DateTimeField(
        _("Sent to review at"),
        blank=True,
        null=True,
    )
    sent_to_review_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name=_("Sent to review by"),
        blank=True,
        null=True,
        on_delete=models.PROTECT,
        related_name="+",
    )
    sent_to_activation_at = models.DateTimeField(
        _("Sent to activation at"),
        blank=True,
        null=True,
    )
    sent_to_activation_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name=_("Sent to activation by"),
        blank=True,
        null=True,
        on_delete=models.PROTECT,
        related_name="+",
    )
    activated_at = models.DateTimeField(
        _("Activated at"),
        blank=True,
        null=True,
    )
    activated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name=_("Activated by"),
        blank=True,
        null=True,
        on_delete=models.PROTECT,
        related_name="+",
    )

    status: VersionStatus = models.CharField(
        _("Status"),
        choices=VersionStatus.choices,
        default=VersionStatus.DRAFT,
    )

    class Meta:
        abstract = True
        ordering = ("id",)

    def save(self, *args, **kwargs):
        if self._state.adding and not self.created_at:
            self.created_at = timezone.now()

        if self.status == VersionStatus.DRAFT:
            self.modified_at = timezone.now()

        super().save(*args, **kwargs)

    def change_status(
        self,
        transition: VersionTransition,
        user: User,
        to_user_id: int = None,
    ):
        if transition == VersionTransition.TO_REVIEW:
            if not (self.created_by == user or is_editor_or_higher(user)):
                raise PermissionDenied("MISSING_AUTHORIZATION")

            self.status = VersionStatus.REVIEW
            self.sent_to_review_at = timezone.now()
            self.sent_to_review_by = user
            self.save()

        elif transition == VersionTransition.TO_ACTIVATION:
            if not is_editor_or_higher(user):
                raise PermissionDenied("MISSING_AUTHORIZATION")

            self.status = VersionStatus.ACTIVATION
            self.sent_to_activation_at = timezone.now()
            self.sent_to_activation_by = user
            self.save()

        elif transition == VersionTransition.ACTIVATE:
            if not is_admin(user):
                raise PermissionDenied("MISSING_AUTHORIZATION")

            self.status = VersionStatus.ACTIVATED
            self.activated_at = timezone.now()
            self.activated_by = user
            self.save()

        elif transition == VersionTransition.TO_DRAFT:
            if not is_editor_or_higher(user):
                raise PermissionDenied("MISSING_AUTHORIZATION")

            self.copy_to_new_draft(to_user_id)

        else:
            raise ParseError("Invalid transition")

    def copy_to_new_draft(self, created_by_id: int) -> None:
        now = timezone.now()

        self.id = None  # marks self as new
        self.status = VersionStatus.DRAFT
        self.created_at = now
        self.created_by_id = created_by_id
        self.modified_at = now
        self.modified_by_id = created_by_id
        self.sent_to_review_at = None
        self.sent_to_review_by = None
        self.sent_to_activation_at = None
        self.sent_to_activation_by = None
        self.activated_at = None
        self.activated_by = None


class BaseWorkflowInfo(models.Model):
    from_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="+",
    )
    to_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="+",
    )
    status_before: VersionStatus | None = models.CharField(
        choices=VersionStatus.choices,
        null=True,
        blank=True,
    )
    status_after: VersionStatus | None = models.CharField(
        choices=VersionStatus.choices,
        null=True,
        blank=True,
    )
    timestamp = models.DateTimeField(default=timezone.now)
    comment = models.TextField(blank=True)
    replies = PydanticJSONField(
        null=True,
        default=list,
        validators=[SchemaValidator(schema=schema.WFIReplySchema)],
    )
    resolved = models.BooleanField(default=False)

    class Meta:
        abstract = True
        ordering = ("-timestamp",)

    def get_object_url(self):
        _site = Site.objects.get(is_default_site=True)
        _port = f":{_site.port}" if _site.port not in [80, 443] else ""
        base_url = f"http{'s' if _site.port == 443 else ''}://{_site.hostname}{_port}"
        return base_url


class BaseDataSource(models.Model):
    nid = NanoIDField("ID", max_length=15, db_index=True)
    type = models.CharField(_("Type"), choices=choices.DATASOURCE_TYPE_CHOICES)
    # NOTE hit a URL > 1000 chars... so going with 5000 for now.
    url = models.URLField(_("Url"), blank=True, max_length=5000)
    file = models.FileField(_("File"), blank=True, null=True, max_length=3000)
    file_not_public = models.BooleanField(_("Keep PDF not public"), default=False)
    publication_title = models.CharField(_("Publication title"), blank=True)
    date = LooseDateField(_("Date"), blank=True, null=True)
    name = models.CharField(_("Name"), blank=True)
    company = models.CharField(_("Organisation"), blank=True)
    email = models.EmailField(_("Email"), blank=True)
    phone = models.CharField(_("Phone"), blank=True)
    includes_in_country_verified_information = models.BooleanField(
        _("Includes in-country-verified information"), blank=True, null=True
    )
    open_land_contracts_id = models.CharField(_("Open Contracting ID"), blank=True)
    comment = models.TextField(_("Comment"), blank=True)

    class Meta:
        abstract = True
        unique_together = ["dealversion", "nid"]
        indexes = [models.Index(fields=["dealversion", "nid"])]
        ordering = ["id"]

    def save(self, *args, **kwargs):
        if self._state.adding and not self.nid:
            self.nid = generate(size=8)
        super().save(*args, **kwargs)
