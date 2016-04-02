__author__ = 'Lene Preuss <lp@sinnwerkstatt.com>'

from grid.forms.base_form import BaseForm
from grid.widgets import TitleField, NumberInput, CommentInput, YearBasedIntegerField

from django import forms
from django.utils.translation import ugettext_lazy as _


class ChangeDealEmploymentForm(BaseForm):

    form_title = _('Employment')

    tg_total_number_of_jobs_created = TitleField(required=False, label="", initial=_("Number of total jobs created"))
    total_jobs_created = forms.BooleanField(required=False, label=_("Total number of jobs created"))
    total_jobs_planned = forms.IntegerField(required=False, label=_("Planned total number of jobs"), help_text=_("jobs"), widget=NumberInput)
    total_jobs_planned_employees = forms.IntegerField(required=False, label=_("Employees"), help_text=_("employees"), widget=NumberInput)
    total_jobs_planned_daily_workers = forms.IntegerField(required=False, label=_("Daily/seasonal  workers"), help_text=_("workers"), widget=NumberInput)
    total_jobs_current = YearBasedIntegerField(required=False, label=_("Current total number of jobs"), help_text=_("jobs"), widget=NumberInput)
    total_jobs_current_employees = YearBasedIntegerField(required=False, label=_("Current total employees"), help_text=_("employees"), widget=NumberInput)
    total_jobs_current_daily_workers = YearBasedIntegerField(required=False, label=_("Daily/seasonal  workers"), help_text=_("workers"), widget=NumberInput)
    tg_total_number_of_jobs_created_comment = forms.CharField(required=False, label=_("Additional comments"), widget=CommentInput)

    tg_foreign_jobs_created = TitleField(required=False, label="", initial=_("Number of jobs for foreigners created"))
    foreign_jobs_created = forms.BooleanField(required=False, label=_("Number of jobs for foreigners created"))
    foreign_jobs_planned = forms.IntegerField(required=False, label=_("Planned number of jobs for foreigners"), help_text=_("jobs"), widget=NumberInput)
    foreign_jobs_planned_employees = forms.IntegerField(required=False, label=_("Employees"), help_text=_("employees"), widget=NumberInput)
    foreign_jobs_planned_daily_workers = forms.IntegerField(required=False, label=_("Daily/seasonal workers"), help_text=_("workers"), widget=NumberInput)
    foreign_jobs_current = YearBasedIntegerField(required=False, label=_("Current number of jobs for foreigners"), help_text=_("jobs"))
    foreign_jobs_current_employees = YearBasedIntegerField(required=False, label=_("Employees"), help_text=_("employees"))
    foreign_jobs_current_daily_workers = YearBasedIntegerField(required=False, label=_("Daily/seasonal workers"), help_text=_("workers"))
    tg_foreign_jobs_created_comment = forms.CharField(required=False, label=_("Additional comments"), widget=CommentInput)

    tg_domestic_jobs_created = TitleField(required=False, label="", initial=_("Number of domestic jobs created"))
    domestic_jobs_created = forms.BooleanField(required=False, label=_("Number of domestic jobs created"))
    domestic_jobs_planned = forms.IntegerField(required=False, label=_("Planned number of domestic jobs"), help_text=_("jobs"), widget=NumberInput)
    domestic_jobs_planned_employees = forms.IntegerField(required=False, label=_("Employees"), help_text=_("employees"), widget=NumberInput)
    domestic_jobs_planned_daily_workers = forms.IntegerField(required=False, label=_("Daily/seasonal workers"), help_text=_("workers"), widget=NumberInput)
    domestic_jobs_current = YearBasedIntegerField(required=False, label=_("Current number of domestic jobs"), help_text=_("jobs"))
    domestic_jobs_current_employees = YearBasedIntegerField(required=False, label=_("Employees"), help_text=_("employees"))
    domestic_jobs_current_daily_workers = YearBasedIntegerField(required=False, label=_("Daily/seasonal workers"), help_text=_("workers"))
    tg_domestic_jobs_created_comment = forms.CharField(required=False, label=_("Additional comments"), widget=CommentInput)

    class Meta:
        name = 'employment'
