from django import forms
from django.utils.translation import ugettext_lazy as _

from .base_form import BaseForm
from grid.widgets import (
    TitleField, CommentInput, NumberInput, YearBasedIntegerField,
)


__author__ = 'Lene Preuss <lp@sinnwerkstatt.com>'


class DealEmploymentForm(BaseForm):

    form_title = _('Employment')

    # Total number of jobs created
    tg_total_number_of_jobs_created = TitleField(
        required=False, label="", initial=_("Number of total jobs created"))
    total_jobs_created = forms.BooleanField(
        required=False, label=_("Jobs created (total)"))
    total_jobs_planned = forms.IntegerField(
        required=False, label=_("Planned number of jobs (total)"),
        help_text=_("jobs"), widget=NumberInput)
    total_jobs_planned_employees = forms.IntegerField(
        required=False, label=_("Planned employees (total)"), help_text=_("employees"),
        widget=NumberInput)
    total_jobs_planned_daily_workers = forms.IntegerField(
        required=False, label=_("Planned daily/seasonal workers (total)"),
        help_text=_("workers"), widget=NumberInput)
    total_jobs_current = YearBasedIntegerField(
        required=False, label=_("Current number of jobs (total)"),
        help_text=_("jobs"), widget=NumberInput)
    total_jobs_current_employees = YearBasedIntegerField(
        required=False, label=_("Current number of employees (total)"),
        help_text=_("employees"), widget=NumberInput)
    total_jobs_current_daily_workers = YearBasedIntegerField(
        required=False, label=_("Current number of daily/seasonal workers (total)"),
        help_text=_("workers"), widget=NumberInput)
    tg_total_number_of_jobs_created_comment = forms.CharField(
        required=False, label=_("Comment on jobs created (total)"),
        widget=CommentInput)

    # Number of jobs for foreigners created
    tg_foreign_jobs_created = TitleField(
        required=False, label="",
        initial=_("Number of jobs for foreigners created"))
    foreign_jobs_created = forms.BooleanField(
        required=False, label=_("Jobs created (foreign)"))
    foreign_jobs_planned = forms.IntegerField(
        required=False, label=_("Planned number of jobs (foreign)"),
        help_text=_("jobs"), widget=NumberInput)
    foreign_jobs_planned_employees = forms.IntegerField(
        required=False, label=_("Planned employees (foreign)"), help_text=_("employees"),
        widget=NumberInput)
    foreign_jobs_planned_daily_workers = forms.IntegerField(
        required=False, label=_("Planned daily/seasonal workers (foreign)"),
        help_text=_("workers"), widget=NumberInput)
    foreign_jobs_current = YearBasedIntegerField(
        required=False, label=_("Current number of jobs (foreign)"),
        help_text=_("jobs"))
    foreign_jobs_current_employees = YearBasedIntegerField(
        required=False, label=_("Current number of employees (foreign)"), help_text=_("employees"))
    foreign_jobs_current_daily_workers = YearBasedIntegerField(
        required=False, label=_("Current number of daily/seasonal workers (foreign)"),
        help_text=_("workers"))
    tg_foreign_jobs_created_comment = forms.CharField(
        required=False, label=_("Comment on jobs created (foreign)"),
        widget=CommentInput)

    # Number of domestic jobs created
    tg_domestic_jobs_created = TitleField(
        required=False, label="", initial=_("Number of domestic jobs created"))
    domestic_jobs_created = forms.BooleanField(
        required=False, label=_("Jobs created (domestic)"))
    domestic_jobs_planned = forms.IntegerField(
        required=False, label=_("Planned number of jobs (domestic)"),
        help_text=_("jobs"), widget=NumberInput)
    domestic_jobs_planned_employees = forms.IntegerField(
        required=False, label=_("Planned employees (domestic)"), help_text=_("employees"),
        widget=NumberInput)
    domestic_jobs_planned_daily_workers = forms.IntegerField(
        required=False, label=_("Planned daily/seasonal workers (domestic)"),
        help_text=_("workers"), widget=NumberInput)
    domestic_jobs_current = YearBasedIntegerField(
        required=False, label=_("Current number of jobs (domestic)"),
        help_text=_("jobs"))
    domestic_jobs_current_employees = YearBasedIntegerField(
        required=False, label=_("Current number of employees (domestic)"), help_text=_("employees"))
    domestic_jobs_current_daily_workers = YearBasedIntegerField(
        required=False, label=_("Current number of daily/seasonal workers (domestic)"),
        help_text=_("workers"))
    tg_domestic_jobs_created_comment = forms.CharField(
        required=False, label=_("Comment on jobs created (domestic)"),
        widget=CommentInput)

    class Meta:
        name = 'employment'


class DealEmploymentPublicForm(DealEmploymentForm):
    '''
    TODO: this doesn't seem to actually be used anywhere. Confirm and remove.
    '''
    class Meta:
        fields = (
            "tg_foreign_jobs_created", "foreign_jobs_created",
            "foreign_jobs_planned", "tg_foreign_jobs_created_comment",
            "tg_domestic_jobs_created", "domestic_jobs_created",
            "domestic_jobs_planned", "tg_domestic_jobs_created_comment",
        )
