from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models, transaction
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from django_prometheus.models import ExportModelOperationsMixin
from multiselectfield import MultiSelectField


class InvestorQuerySet(models.QuerySet):
    def public(self, user=None):
        """
        Status public, not to be confused with is_public.
        """
        if user and user.is_authenticated:
            return self.filter(
                models.Q(fk_status_id__in=InvestorBase.PUBLIC_STATUSES)
                | models.Q(history_user=user)
            )
        else:
            return self.filter(fk_status_id__in=InvestorBase.PUBLIC_STATUSES)

    def public_or_deleted(self, user=None):
        statuses = InvestorBase.PUBLIC_STATUSES + (InvestorBase.STATUS_DELETED,)
        if user and user.is_authenticated:
            return self.filter(
                models.Q(fk_status_id__in=statuses) | models.Q(history_user=user)
            )
        else:
            return self.filter(fk_status_id__in=statuses)

    def public_or_pending(self):
        statuses = InvestorBase.PUBLIC_STATUSES + (InvestorBase.STATUS_PENDING,)
        return self.filter(fk_status_id__in=statuses)

    def public_deleted_or_pending(self):
        statuses = InvestorBase.PUBLIC_STATUSES + (
            InvestorBase.STATUS_DELETED,
            InvestorBase.STATUS_PENDING,
        )
        return self.filter(fk_status_id__in=statuses)

    def pending(self):
        statuses = (InvestorBase.STATUS_PENDING, InvestorBase.STATUS_TO_DELETE)
        return self.filter(fk_status_id__in=statuses)

    def pending_only(self):
        return self.filter(fk_status_id=InvestorBase.STATUS_PENDING)

    def active(self):
        return self.filter(fk_status_id=InvestorBase.STATUS_ACTIVE)

    def overwritten(self):
        return self.filter(fk_status_id=InvestorBase.STATUS_OVERWRITTEN)

    def to_delete(self):
        return self.filter(fk_status_id=InvestorBase.STATUS_TO_DELETE)

    def deleted(self):
        return self.filter(fk_status_id=InvestorBase.STATUS_DELETED)

    def rejected(self):
        return self.filter(fk_status_id=InvestorBase.STATUS_REJECTED)


class InvestorBase(models.Model):
    # FIXME: Replace fk_status with Choice Field
    STATUS_PENDING = 1
    STATUS_ACTIVE = 2
    STATUS_OVERWRITTEN = 3
    STATUS_DELETED = 4
    STATUS_REJECTED = 5
    STATUS_TO_DELETE = 6
    PUBLIC_STATUSES = (STATUS_ACTIVE, STATUS_OVERWRITTEN)
    STATUS_CHOICES = (
        (STATUS_PENDING, _("Pending")),
        (STATUS_ACTIVE, _("Active")),
        (STATUS_OVERWRITTEN, _("Overwritten")),
        (STATUS_DELETED, _("Deleted")),
        (STATUS_REJECTED, _("Rejected")),
        (STATUS_TO_DELETE, _("To delete")),
    )
    INVESTOR_IDENTIFIER_DEFAULT = 2147483647  # max safe int
    STAKEHOLDER_CLASSIFICATIONS = (
        ("10", _("Private company")),
        ("20", _("Stock-exchange listed company")),
        ("30", _("Individual entrepreneur")),
        ("40", _("Investment fund")),
        ("50", _("Semi state-owned company")),
        ("60", _("State-/government (owned) company")),
        ("70", _("Other (please specify in comment field)")),
    )
    INVESTOR_CLASSIFICATIONS = (
        ("110", _("Government")),
        ("120", _("Government institution")),
        ("130", _("Multilateral Development Bank (MDB)")),
        ("140", _("Bilateral Development Bank / Development Finance Institution")),
        ("150", _("Commercial Bank")),
        ("160", _("Investment Bank")),
        (
            "170",
            _(
                "Investment Fund (all types incl. pension, hedge, mutual, private equity funds etc.)"
            ),
        ),
        ("180", _("Insurance firm")),
        ("190", _("Private equity firm")),
        ("200", _("Asset management firm")),
        ("210", _("Non - Profit organization (e.g. Church, University etc.)")),
    )
    CLASSIFICATION_CHOICES = STAKEHOLDER_CLASSIFICATIONS + INVESTOR_CLASSIFICATIONS
    ROLE_OPERATING_COMPANY = "OP"
    ROLE_PARENT_COMPANY = "ST"
    ROLE_TERTIARY_INVESTOR = "IN"
    ROLE_CHOICES = (
        (ROLE_OPERATING_COMPANY, _("Operating company")),
        (ROLE_PARENT_COMPANY, _("Parent company")),
        (ROLE_TERTIARY_INVESTOR, _("Tertiary investor/lender")),
    )

    investor_identifier = models.IntegerField(
        _("Investor ID"), db_index=True, default=INVESTOR_IDENTIFIER_DEFAULT
    )
    name = models.CharField(_("Name"), max_length=1024)
    fk_country = models.ForeignKey(
        "Country",
        verbose_name=_("Country of registration/origin"),
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
    )
    classification = models.CharField(
        verbose_name=_("Classification"),
        max_length=3,
        choices=CLASSIFICATION_CHOICES,
        blank=True,
        null=True,
    )

    homepage = models.URLField(_("Investor homepage"), blank=True, null=True)
    opencorporates_link = models.URLField(
        _("Opencorporates link"), blank=True, null=True
    )
    comment = models.TextField(_("Comment"), blank=True, null=True)

    fk_status = models.ForeignKey(
        "Status", verbose_name=_("Status"), on_delete=models.PROTECT
    )

    objects = InvestorQuerySet.as_manager()

    class Meta:
        ordering = ("name",)
        abstract = True

    def __str__(self):
        return "%s (#%i)" % (self.name, self.investor_identifier)

    @classmethod
    def get_next_investor_identifier(cls):
        queryset = cls.objects  # .using('v2')
        queryset = queryset.exclude(investor_identifier=cls.INVESTOR_IDENTIFIER_DEFAULT)
        queryset = queryset.aggregate(models.Max("investor_identifier"))
        return (queryset["investor_identifier__max"] or 0) + 1

    def save(self, *args, **kwargs):
        """
        investor_identifier needs to be set to the PK, which we don't yet have
        for new records. So, set it to a default and then update.

        This is not super efficient (updating an index column twice)
        and may result in duplicate investor_identifiers due to crash or
        query timing, but it should be good enough for our purposes.

        Same thing goes for the name.
        """
        update_fields = []

        if self.investor_identifier is None:
            self.investor_identifier = self.INVESTOR_IDENTIFIER_DEFAULT

        super().save(*args, **kwargs)

        if self.investor_identifier == self.INVESTOR_IDENTIFIER_DEFAULT:
            self.investor_identifier = self.__class__.get_next_investor_identifier()
            update_fields.append("investor_identifier")

        if not self.name or self.name == "Unknown (#{})".format(
            self.investor_identifier
        ):
            self.name = self._get_default_name()
            update_fields.append("name")

        if update_fields:
            super().save(update_fields=update_fields)

    def _get_default_name(self):
        """
        If we have an unknown (blank) name, get the correct generic text.
        """
        if self.is_operating_company:
            name = _("Unknown operating company (#%s)") % (self.investor_identifier,)
        elif self.is_parent_company:
            name = _("Unknown parent company (#%s)") % (self.investor_identifier,)
        elif self.is_parent_investor:
            name = _("Unknown tertiary investor/lender (#%s)") % (
                self.investor_identifier,
            )
        else:
            # Just stick with unknown if no relations
            name = _("Unknown (#%s)") % (self.investor_identifier,)

        return name

    def get_history(self, user=None):
        """
        Returns all deal versions
        """
        queryset = HistoricalInvestor.objects.filter(
            investor_identifier=self.investor_identifier
        )
        if not (user and user.is_authenticated):
            queryset = queryset.filter(
                fk_status__in=(
                    HistoricalInvestor.STATUS_ACTIVE,
                    HistoricalInvestor.STATUS_OVERWRITTEN,
                )
            )
        return queryset.order_by("-history_date")

    @property
    def is_operating_company(self):
        """
        Moved this logic from the view. Not sure though if we should
        determine this using classification in future.
        """
        return hasattr(self, "involvements") and self.involvements.exists()

    @property
    def is_parent_company(self):
        """
        Right now, this is determined based on if any relations exist.
        It probably makes more sense to have this as a flag on the model.
        """
        if hasattr(self, "investors"):
            queryset = self.investors.all()
            queryset = queryset.filter(
                role=HistoricalInvestorVentureInvolvement.STAKEHOLDER_ROLE
            )
            return queryset.exists()
        else:  # pragma: no cover
            return False

    @property
    def is_parent_investor(self):
        if hasattr(self, "investors"):
            queryset = self.investors.all()
            queryset = queryset.filter(
                role=HistoricalInvestorVentureInvolvement.INVESTOR_ROLE
            )
            return queryset.exists()
        else:  # pragma: no cover
            return False

    @classmethod
    def get_latest_investor(cls, investor_identifier):
        return (
            cls.objects.filter(investor_identifier=investor_identifier)
            .order_by("-id")
            .first()
        )

    @classmethod
    def get_latest_active_investor(cls, investor_identifier):
        return (
            cls.objects.filter(investor_identifier=investor_identifier)
            .filter(fk_status__name__in=("active", "overwritten", "deleted"))
            .order_by("-id")
            .first()
        )

    def format_investors(self, investors):
        # First name, then ID to be able to sort by name
        return "|".join(
            [
                "#".join(
                    [
                        i.name.replace("#", "").replace("\n", "").strip(),
                        str(i.investor_identifier),
                        (i.fk_country and i.fk_country.name or ""),
                    ]
                )
                for i in investors
            ]
        )

    def get_deal_count(self):
        from apps.landmatrix.models import HistoricalActivity

        latest_ids = HistoricalActivity.objects.latest_ids(
            status=HistoricalActivity.PUBLIC_STATUSES
        )
        return self.involvements.filter(fk_activity_id__in=latest_ids).count()

    def get_roles(self):
        roles = []
        # Operating company?
        if self.involvements.filter(fk_activity__fk_status__in=(2, 3)).count() > 0:
            roles.append(InvestorBase.ROLE_OPERATING_COMPANY)
        # Parent company?
        if (
            self.investors.filter(
                role=HistoricalInvestorVentureInvolvement.STAKEHOLDER_ROLE
            ).count()
            > 0
        ):
            roles.append(InvestorBase.ROLE_PARENT_COMPANY)
        # Tertiary investor/lender?
        if (
            self.investors.filter(
                role=HistoricalInvestorVentureInvolvement.INVESTOR_ROLE
            ).count()
            > 0
        ):
            roles.append(InvestorBase.ROLE_TERTIARY_INVESTOR)
        return roles

    def get_latest(self, user=None):
        """
        Returns latest historical activity
        """
        queryset = self.get_history(user)
        return queryset.latest()

    def is_editable(self, user=None):
        if user and user.is_authenticated:
            if self.get_latest(user) != self:
                # Only superuser are allowed to edit old versions
                if user and user.is_superuser:
                    return True
                return False
            # Status: Pending
            is_editor = user.has_perm("landmatrix.review_historicalactivity")
            is_author = self.history_user_id == user.id
            # Only Editors and Administrators are allowed to edit pending deals
            if is_editor:
                return True
            else:
                if self.fk_status_id in (self.STATUS_PENDING, self.STATUS_TO_DELETE):
                    return False
                elif self.fk_status_id == self.STATUS_REJECTED and not is_author:
                    return False
                else:
                    return True
        return False


class HistoricalInvestorQuerySet(InvestorQuerySet):
    def get_for_user(self, user):
        qs = self.filter(history_user=user).values_list(
            "investor_identifier", flat=True
        )
        return self.filter(investor_identifier__in=qs).filter(id__in=self.latest_ids())

    def _single_revision_identifiers(self):
        """
        Get all investor identifiers (as values) that only have a single
        revision.

        This query looks a bit strange, but the order of operations is required
        in order to construct the group by correctly.
        """
        queryset = HistoricalInvestor.objects.values(
            "investor_identifier"
        )  # don't use 'self' here
        queryset = queryset.annotate(
            revisions_count=models.Count("investor_identifier")
        )
        queryset = queryset.order_by("investor_identifier")
        queryset = queryset.exclude(revisions_count__gt=1)
        queryset = queryset.values_list("investor_identifier", flat=True)

        return queryset

    def with_multiple_revisions(self):
        """
        Get only new investors (without any other historical instances).
        """
        subquery = self._single_revision_identifiers()
        queryset = self.exclude(investor_identifier__in=subquery)
        return queryset.filter(id__in=self.latest_ids())

    def without_multiple_revisions(self):
        """
        Get only new investors (without any other historical instances).
        """
        subquery = self._single_revision_identifiers()
        queryset = self.filter(investor_identifier__in=subquery)
        return queryset.filter(id__in=self.latest_ids())

    def latest_ids(self, status=None):
        queryset = HistoricalInvestor.objects
        if status:
            queryset = queryset.filter(fk_status_id__in=status)
        queryset = queryset.values("investor_identifier").annotate(
            max_id=models.Max("id")
        )
        queryset = queryset.order_by().values_list("max_id", flat=True)
        return queryset

    def latest_only(self, status=None):
        return self.filter(id__in=self.latest_ids(status))

    def latest_public_or_pending(self):
        return self.filter(
            id__in=self.latest_ids(
                status=(
                    HistoricalInvestor.STATUS_ACTIVE,
                    HistoricalInvestor.STATUS_OVERWRITTEN,
                    HistoricalInvestor.STATUS_PENDING,
                )
            )
        )

    def latest_public_and_pending(self):
        public_filter = models.Q(
            id__in=self.latest_ids(
                status=(
                    HistoricalInvestor.STATUS_ACTIVE,
                    HistoricalInvestor.STATUS_OVERWRITTEN,
                )
            )
        )
        public_or_pending_filter = models.Q(
            id__in=self.latest_ids(
                status=(
                    HistoricalInvestor.STATUS_ACTIVE,
                    HistoricalInvestor.STATUS_OVERWRITTEN,
                    HistoricalInvestor.STATUS_PENDING,
                )
            )
        )
        return self.filter(public_filter | public_or_pending_filter)


class HistoricalInvestor(ExportModelOperationsMixin("investor"), InvestorBase):
    history_date = models.DateTimeField(default=timezone.now)
    history_user = models.ForeignKey(
        "auth.User", blank=True, null=True, on_delete=models.SET_NULL
    )
    action_comment = models.TextField(_("Comment"), blank=True, null=True)

    objects = HistoricalInvestorQuerySet.as_manager()

    def approve_change(self, user=None, comment=None):
        if self.fk_status_id != HistoricalInvestor.STATUS_PENDING:  # pragma: no cover
            return

        # Only approvals of administrators should go public
        if user.has_perm("landmatrix.change_historicalactivity"):
            # TODO: this logic is taken from changeset protocol
            # but it won't really work properly. We need to determine behaviour
            # when updates happen out of order. There can easily be many edits,
            # and not the latest one is approved.
            latest_public_version = self.__class__.get_latest_active_investor(
                self.investor_identifier
            )
            if latest_public_version:
                self.fk_status_id = HistoricalInvestor.STATUS_OVERWRITTEN
            else:
                self.fk_status_id = HistoricalInvestor.STATUS_ACTIVE
            self.save(update_fields=["fk_status"])

            self.update_public_investor()

    def reject_change(self, user=None, comment=None):
        if self.fk_status_id != HistoricalInvestor.STATUS_PENDING:  # pragma: no cover
            return
        self.fk_status_id = HistoricalInvestor.STATUS_REJECTED
        self.save(update_fields=["fk_status"])
        # self.update_public_investor() - don't update public investor

    def approve_delete(self, user=None, comment=None):
        if self.fk_status_id != HistoricalInvestor.STATUS_TO_DELETE:  # pragma: no cover
            return
        # Only approvals of administrators should be deleted
        if user.has_perm("landmatrix.delete_historicalactivity"):
            self.fk_status_id = HistoricalInvestor.STATUS_DELETED
            self.save(update_fields=["fk_status"])
            self.update_public_investor()

    def reject_delete(self, user=None, comment=None):
        if self.fk_status_id != HistoricalInvestor.STATUS_TO_DELETE:  # pragma: no cover
            return
        self.fk_status_id = HistoricalInvestor.STATUS_REJECTED
        self.save(update_fields=["fk_status"])

    def get_top_investors(self):
        """
        Get list of highest parent companies (all right-hand side parent companies of the network
        visualisation)
        """
        investors_processed = set()

        def get_parent_companies(investors):
            parents = []
            for investor in investors:
                if investor.id in investors_processed:
                    parents.append(investor)
                    continue
                else:
                    investors_processed.add(investor.id)
                # Check if there are parent companies for investor
                queryset = HistoricalInvestorVentureInvolvement.objects.filter(
                    fk_venture=investor,
                    fk_venture__fk_status__in=(
                        InvestorBase.STATUS_ACTIVE,
                        InvestorBase.STATUS_OVERWRITTEN,
                    ),
                    fk_investor__fk_status__in=(
                        InvestorBase.STATUS_ACTIVE,
                        InvestorBase.STATUS_OVERWRITTEN,
                    ),
                    role=HistoricalInvestorVentureInvolvement.STAKEHOLDER_ROLE,
                ).exclude(fk_investor=investor)
                queryset = queryset.select_related(
                    "fk_investor", "fk_investor__fk_country"
                ).defer("fk_investor__fk_country__geom")
                parent_companies = [ivi.fk_investor for ivi in queryset]
                if parent_companies:
                    parents.extend(get_parent_companies(parent_companies))
                elif investor.fk_status_id in (
                    InvestorBase.STATUS_ACTIVE,
                    InvestorBase.STATUS_OVERWRITTEN,
                ):
                    parents.append(investor)
            return parents

        top_investors = list(set(get_parent_companies([self])))
        return top_investors

    def update_public_investor(self, approve=True):
        """
        Recursively update investor chain
        :param approve: Approve pending investors (only if first version)
        :return:
        """
        # Keep track of investor identifiers to prevent infinite loops
        investor_identifiers = []

        def update_investor(hinv, approve=True):
            versions = HistoricalInvestor.objects.filter(
                investor_identifier=hinv.investor_identifier
            )
            versions = versions.exclude(
                fk_status_id__in=(hinv.STATUS_PENDING, hinv.STATUS_TO_DELETE)
            )
            # Only approve if all existing versions are pending
            if approve and versions.count() == 0:
                # Update status of historical investor
                if hinv.fk_status_id == hinv.STATUS_PENDING:
                    hinv.fk_status_id = hinv.STATUS_OVERWRITTEN
                elif hinv.fk_status_id == hinv.STATUS_TO_DELETE:
                    hinv.fk_status_id = hinv.STATUS_DELETED
                hinv.save()

            if hinv.investor_identifier in investor_identifiers:
                return
            else:
                investor_identifiers.append(hinv.investor_identifier)

            # Investor has been deleted?
            if self.fk_status_id == self.STATUS_DELETED:
                return
            elif self.fk_status_id == self.STATUS_REJECTED:
                # Investor add has been rejected?
                investors = HistoricalInvestor.objects.filter(
                    investor_identifier=self.investor_identifier
                )
                if len(investors) == 1:
                    return

            for hinvolvement in hinv.venture_involvements.all():
                # Update InvestorVentureInvolvement
                hinvolvement.fk_status_id = hinv.STATUS_OVERWRITTEN
                hinvolvement.save()
                # Update investor
                update_investor(hinvolvement.fk_investor, approve=approve)

        update_investor(self, approve=approve)
        self.update_current_involvements()

    def update_current_involvements(self):
        # Update all current involvements (linking to the old investor version) to the new investor version
        queryset = (
            HistoricalInvestorActivityInvolvement.objects.for_current_activities()
        )
        queryset = queryset.filter(
            fk_investor__investor_identifier=self.investor_identifier
        )
        queryset = queryset.exclude(fk_investor_id=self.id)
        for involvement in queryset:
            involvement.fk_investor_id = self.id
            involvement.save()

    def save(self, *args, **kwargs):
        update_elasticsearch = kwargs.pop("update_elasticsearch", True)
        super().save(*args, **kwargs)
        if update_elasticsearch and settings.OLD_ELASTIC:
            from apps.landmatrix.tasks import index_investor, delete_historicalinvestor

            if self.fk_status_id == self.STATUS_DELETED:
                transaction.on_commit(
                    lambda: delete_historicalinvestor.delay(self.investor_identifier)
                )
            else:
                transaction.on_commit(
                    lambda: index_investor.delay(self.investor_identifier)
                )

            from apps.landmatrix.tasks import task_propagate_save_to_gnd_investor

            task_propagate_save_to_gnd_investor(self.pk)

    class Meta:
        verbose_name = _("Historical investor")
        verbose_name_plural = _("Historical investors")
        get_latest_by = "history_date"
        ordering = ["-history_date"]
        permissions = (("review_historicalinvestor", "Can review investor changes"),)


class InvestorVentureQuerySet(models.QuerySet):
    ACTIVE_STATUS_NAMES = ("pending", "active", "overwritten")

    def active(self):
        return self.filter(fk_status__name__in=self.ACTIVE_STATUS_NAMES)

    def latest_only(self, status=None):
        latest_ids = HistoricalInvestor.objects.latest_ids(status=status)
        return self.filter(fk_venture_id__in=latest_ids, fk_investor_id__in=latest_ids)

    def latest_only_public_status(self):
        latest_ids = HistoricalInvestor.objects.latest_ids(
            status=HistoricalInvestor.PUBLIC_STATUSES
        )
        return self.filter(fk_venture_id__in=latest_ids, fk_investor_id__in=latest_ids)

    # deprecated
    def stakeholders(self):
        return self.parent_companies()

    # deprecated
    def investors(self):
        return self.tertiary_investors()

    def parent_companies(self):
        return self.filter(role=HistoricalInvestorVentureInvolvement.STAKEHOLDER_ROLE)

    def tertiary_investors(self):
        return self.filter(role=HistoricalInvestorVentureInvolvement.INVESTOR_ROLE)


class InvestorVentureInvolvementBase(models.Model):
    """
    InvestorVentureInvolvement links investors to each other.
    Generally fk_venture links to the Operating company, and fk_investor
    links to investors or parent stakeholders in that company (depending
    on the role).
    """

    # FIXME: Replace fk_status with Choice Field
    STATUS_PENDING = 1
    STATUS_ACTIVE = 2
    STATUS_OVERWRITTEN = 3
    STATUS_DELETED = 4
    STATUS_REJECTED = 5
    STATUS_TO_DELETE = 6
    PUBLIC_STATUSES = (STATUS_ACTIVE, STATUS_OVERWRITTEN)
    STATUS_CHOICES = (
        STATUS_PENDING,
        _("Pending"),
        STATUS_ACTIVE,
        _("Active"),
        STATUS_OVERWRITTEN,
        _("Overwritten"),
        STATUS_DELETED,
        _("Deleted"),
        STATUS_REJECTED,
        _("Rejected"),
        STATUS_TO_DELETE,
        _("To delete"),
    )
    STAKEHOLDER_ROLE = "ST"
    INVESTOR_ROLE = "IN"
    ROLE_CHOICES = (
        (STAKEHOLDER_ROLE, _("Parent company")),
        (INVESTOR_ROLE, _("Tertiary investor/lender")),
    )
    EQUITY_INVESTMENT_TYPE = 10
    DEBT_FINANCING_INVESTMENT_TYPE = 20
    INVESTMENT_TYPE_CHOICES = (
        (EQUITY_INVESTMENT_TYPE, _("Shares/Equity")),
        (DEBT_FINANCING_INVESTMENT_TYPE, _("Debt financing")),
    )
    PARENT_RELATION_CHOICES = (
        ("Subsidiary", _("Subsidiary of parent company")),
        ("Local branch", _("Local branch of parent company")),
        ("Joint venture", _("Joint venture of parent companies")),
    )

    role = models.CharField(
        verbose_name=_("Relation type"), max_length=2, choices=ROLE_CHOICES
    )
    investment_type = MultiSelectField(
        max_length=255,
        choices=INVESTMENT_TYPE_CHOICES,
        default="",
        blank=True,
        null=True,
    )
    percentage = models.FloatField(
        _("Ownership share"),
        blank=True,
        null=True,
        validators=[MinValueValidator(0.0), MaxValueValidator(100.0)],
    )
    loans_amount = models.FloatField(_("Loan amount"), blank=True, null=True)
    loans_currency = models.ForeignKey(
        "Currency",
        verbose_name=_("Loan currency"),
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
    )
    loans_date = models.CharField("Loan date", max_length=10, blank=True, null=True)
    parent_relation = models.CharField(
        verbose_name=_("Parent relation"),
        max_length=255,
        choices=PARENT_RELATION_CHOICES,
        blank=True,
        null=True,
    )
    comment = models.TextField(_("Comment"), blank=True, null=True)

    fk_status = models.ForeignKey(
        "Status", verbose_name=_("Status"), default=1, on_delete=models.PROTECT
    )

    objects = InvestorVentureQuerySet.as_manager()

    class Meta:
        abstract = True


class HistoricalInvestorVentureInvolvement(
    ExportModelOperationsMixin("investor_venture_involvement"),
    InvestorVentureInvolvementBase,
):
    # FIXME: related names are named the wrong way here
    fk_venture = models.ForeignKey(
        HistoricalInvestor,
        verbose_name=_("Investor ID Downstream"),
        db_index=True,
        related_name="venture_involvements",
        on_delete=models.CASCADE,
    )
    fk_investor = models.ForeignKey(
        HistoricalInvestor,
        verbose_name=_("Investor ID Upstream"),
        db_index=True,
        related_name="investors",
        on_delete=models.CASCADE,
    )

    class Meta:
        verbose_name = _("Historical Investor Venture Involvement")
        verbose_name_plural = _("Historical Investor Venture Involvements")
        get_latest_by = "-id"


class InvestorActivityInvolvementManager(models.Manager):
    def for_current_activities(self, user_is_editor=False):
        """
        Get involvements for newest versions of activities
        :return:
        """
        activity_class = self.model._meta.get_field("fk_activity").related_model
        stati = [1, 2, 3, 6] if user_is_editor else [2, 3]
        current_activities = activity_class.objects.latest_ids(status=stati)
        return self.filter(fk_activity_id__in=current_activities)


class InvestorActivityInvolvementBase(models.Model):
    """
    InvestorActivityInvolvments link Operational Companies (Investor model)
    to activities.

    There should only be one Operating company per activity,
    although this is not enforced by the model currently. Other investors
    are then linked to the Operating company through
    InvestorVentureInvolvement.
    """

    # FIXME: Replace fk_status with Choice Field
    STATUS_PENDING = 1
    STATUS_ACTIVE = 2
    STATUS_OVERWRITTEN = 3
    STATUS_DELETED = 4
    STATUS_REJECTED = 5
    STATUS_TO_DELETE = 6
    STATUS_CHOICES = (
        STATUS_PENDING,
        _("Pending"),
        STATUS_ACTIVE,
        _("Active"),
        STATUS_OVERWRITTEN,
        _("Overwritten"),
        STATUS_DELETED,
        _("Deleted"),
        STATUS_REJECTED,
        _("Rejected"),
        STATUS_TO_DELETE,
        _("To delete"),
    )

    fk_status = models.ForeignKey(
        "Status", verbose_name=_("Status"), on_delete=models.PROTECT
    )

    objects = InvestorActivityInvolvementManager()

    def __str__(self):
        return "Activity: %i Investor: %i" % (self.fk_activity_id, self.fk_investor_id)

    class Meta:
        abstract = True


class HistoricalInvestorActivityInvolvement(
    ExportModelOperationsMixin("investor_activity_involvement"),
    InvestorActivityInvolvementBase,
):
    fk_activity = models.ForeignKey(
        "HistoricalActivity",
        verbose_name=_("Activity"),
        related_name="involvements",
        db_index=True,
        on_delete=models.CASCADE,
    )
    fk_investor = models.ForeignKey(
        "HistoricalInvestor",
        verbose_name=_("Investor"),
        related_name="involvements",
        db_index=True,
        on_delete=models.CASCADE,
    )

    class Meta:
        verbose_name = _("Historical Investor Activity Involvement")
        verbose_name_plural = _("Historical Investor Activity Involvements")
        ordering = ["-id"]
