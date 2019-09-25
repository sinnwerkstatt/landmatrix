from django.utils.translation import ugettext_lazy as _

from apps.grid.forms.investor_form import (
    OperationalCompanyForm,
    ParentInvestorForm,
    ParentStakeholderForm,
)
from apps.grid.views.utils import DEAL_FORMS
from apps.landmatrix.forms import ActivityFilterForm, InvestorFilterForm


def get_activity_field_by_key(key):
    # Deal fields
    if key in ActivityFilterForm.base_fields:
        return ActivityFilterForm().fields[key]
    # Deal fields
    for form in DEAL_FORMS:
        form = hasattr(form, "form") and form.form or form
        if key in form.base_fields:
            return form().fields[key]
    # Operating company fields
    investor_forms = {
        "operating_company_": OperationalCompanyForm,
        "parent_stakeholder_": ParentStakeholderForm,
        "parent_investor_": ParentInvestorForm,
    }
    for prefix, form in investor_forms.items():
        if prefix in key:
            k = key.replace(prefix, "")
            if k in form.base_fields:
                return form().fields[k]
    return None


def get_investor_field_by_key(key):
    # Investor fields
    if key in InvestorFilterForm.base_fields:
        return InvestorFilterForm().fields[key]
    # Operating company fields
    investor_forms = {
        "parent_stakeholder_": ParentStakeholderForm,
        "parent_investor_": ParentInvestorForm,
    }
    for prefix, form in investor_forms.items():
        if prefix in key:
            k = key.replace(prefix, "")
            if k in form.base_fields:
                return form().fields[k]
    return None


def get_activity_field_label(key):
    CUSTOM_FIELDS = {"activity_identifier": _("Deal ID")}
    if key in CUSTOM_FIELDS.keys():
        return str(CUSTOM_FIELDS[key])
    field = get_activity_field_by_key(key)
    if field:
        investor_labels = {
            "operating_company_": _("Operating company"),
            "parent_stakeholder_": _("Parent company"),
            "parent_investor_": _("Tertiary investor/lender"),
        }
        for prefix, label in investor_labels.items():
            if prefix in key:
                return "%s %s" % (str(label), str(field.label))
        return str(field.label)
    return None


def get_investor_field_label(key):
    CUSTOM_FIELDS = {"investor_identifier": _("Investor ID")}
    if key in CUSTOM_FIELDS.keys():
        return str(CUSTOM_FIELDS[key])
    field = get_investor_field_by_key(key)
    if field:
        investor_labels = {
            "parent_stakeholder_": _("Parent company"),
            "parent_investor_": _("Tertiary investor/lender"),
        }
        for prefix, label in investor_labels.items():
            if prefix in key:
                return "%s %s" % (str(label), str(field.label))
        return str(field.label)
    return None
