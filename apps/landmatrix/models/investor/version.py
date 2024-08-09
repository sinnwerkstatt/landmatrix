import re

from django.db import models
from django.db.models import Q
from django.utils.translation import gettext as _

from apps.accounts.models import User
from apps.landmatrix.models import choices
from apps.landmatrix.models.abstract.version import (
    BaseVersion,
    Action,
    VersionStatus,
)
from apps.landmatrix.models.country import Country


class InvestorVersion(BaseVersion):
    investor = models.ForeignKey(
        "InvestorHull",
        on_delete=models.PROTECT,
        related_name="versions",
    )

    name = models.CharField(_("Name"), blank=True)
    name_unknown = models.BooleanField(default=False)

    country = models.ForeignKey(
        Country,
        verbose_name=_("Country of registration/origin"),
        blank=True,
        null=True,
        on_delete=models.PROTECT,
    )

    classification = models.CharField(
        verbose_name=_("Classification"),
        choices=choices.INVESTOR_CLASSIFICATION_CHOICES,
        blank=True,
        null=True,
    )

    homepage = models.URLField(_("Investor homepage"), blank=True)
    opencorporates = models.URLField(_("Opencorporates link"), blank=True)
    comment = models.TextField(_("Comment"), blank=True)

    # """ Data sources """  via Foreignkey

    """ calculated properties """
    involvements_snapshot = models.JSONField(blank=True, default=list)

    def __str__(self):
        return f"{self.name} (#{self.id})"

    def is_current_draft(self):
        return self.investor.draft_version_id == self.id

    def save(self, *args, **kwargs):
        self._recalculate_fields()
        super().save(*args, **kwargs)

    def _recalculate_fields(self):
        self.name_unknown = bool(
            re.search(r"(unknown|unnamed)", self.name, re.IGNORECASE)
        )

    def change_status(
        self,
        action: Action,
        user: User,
        to_user_id: int = None,
        comment="",
    ):

        old_draft_status = self.status

        super().change_status(action=action, user=user, to_user_id=to_user_id)

        if action == Action.ACTIVATE:
            investor = self.investor
            investor.draft_version = None
            investor.active_version = self

            from apps.landmatrix.models.investor import Involvement

            # upon activation, map the involvements_snapshot into the Involvements table
            seen_involvements = set()
            for invo in self.involvements_snapshot:
                # involvements include bidirectional relations. we filter out only parent relations that we save.
                if invo["child_investor_id"] != investor.id:
                    continue

                try:
                    # TODO: Cleanup magic foo where id as string (nanoId) or None is processed
                    assert isinstance(invo["id"], int)
                    i1 = Involvement.objects.get(id=invo["id"], child_investor=investor)
                except (Involvement.DoesNotExist, AssertionError):
                    i1 = Involvement(child_investor=investor)

                i1.parent_investor_id = invo["parent_investor_id"]
                i1.role = invo["role"]
                i1.investment_type = invo["investment_type"]
                i1.percentage = invo["percentage"]
                i1.loans_amount = invo["loans_amount"]
                i1.loans_currency_id = invo["loans_currency_id"]
                i1.loans_date = invo["loans_date"]
                i1.parent_relation = invo["parent_relation"]
                i1.comment = invo["comment"]
                i1.save()
                seen_involvements.add(i1.id)

            Involvement.objects.filter(child_investor=investor).exclude(
                id__in=seen_involvements
            ).delete()

            investor.save()

            # close unresolved workflowinfos
            self.workflowinfos.all().update(resolved=True)

        elif action == Action.TO_DRAFT:
            investor = self.investor
            investor.draft_version = self
            investor.save()

            # close remaining open feedback requests
            self.workflowinfos.filter(
                Q(
                    status_before__in=[
                        VersionStatus.REVIEW,
                        VersionStatus.ACTIVATION,
                    ]
                )
                & Q(status_after=VersionStatus.DRAFT)
                & (Q(from_user=user) | Q(to_user=user))
            ).update(resolved=True)

        # TODO: REfactor out
        from apps.landmatrix.models.investor import InvestorWorkflowInfo

        InvestorWorkflowInfo.objects.create(
            investor_id=self.investor_id,
            investor_version=self,
            from_user=user,
            to_user_id=to_user_id,
            status_before=old_draft_status,
            status_after=self.status,
            comment=comment,
        )

    def copy_to_new_draft(self, created_by_id: int):
        old_self = InvestorVersion.objects.get(pk=self.pk)

        super().copy_to_new_draft(created_by_id)
        self.save()

        for d1 in old_self.datasources.all():
            d1.id = None
            d1.investorversion = self
            d1.save()
