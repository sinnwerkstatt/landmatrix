__author__ = 'Lene Preuss <lp@sinnwerkstatt.com>'

from grid.forms.base_form import BaseForm
from grid.widgets import TitleField, CommentInput, NumberInput

from django import forms
from django.utils.translation import ugettext_lazy as _


class DealLocalCommunitiesForm(BaseForm):

    form_title = _('Local communities / indigenous peoples')

    # Names of affected communities and indigenous peoples
    tg_names_of_affected = TitleField(
        required=False, label="", initial=_("Names of communities / indigenous peoples affected")
    )
    name_of_community = forms.CharField(
        required=False, label=_("Name of community"), widget=forms.TextInput
    )
    name_of_indigenous_people = forms.CharField(
        required=False, label=_("Name of indigenous people"), widget=forms.TextInput
    )
    tg_affected_comment = forms.CharField(
        required=False, label=_("Additional comments"), widget=CommentInput
    )

    # Recognitions status of community land tenure
    tg_recognition_status = TitleField(
        required=False, label="", initial=_("Recognitions status of community land tenure")
    )
    recognition_status = forms.MultipleChoiceField(
        required=False, label=_("Recognition status of community land tenure"), choices=(
            (_("Indigenous Peoples traditional or customary rights recognized by government"), _("Indigenous Peoples traditional or customary rights recognized by government")),
            (_("Indigenous Peoples traditional or customary rights not recognized by government"), _("Indigenous Peoples traditional or customary rights not recognized by government")),
            (_("Community traditional or customary rights recognized by government"), _("Community traditional or customary rights recognized by government")),
            (_("Community traditional or customary rights not recognized by government"), _("Community traditional or customary rights not recognized by government")),
        ), widget=forms.CheckboxSelectMultiple
    )
    tg_recognition_status_comment = forms.CharField(
        required=False, label=_("Additional comments"), widget=CommentInput
    )

    # Consultation of local community
    tg_community_consultation = TitleField(
        required=False, label="", initial=_("Consultation of local community")
    )
    community_consultation = forms.ChoiceField(
        required=False, label=_("Community consultation"), choices=(
            (_("Not consulted"), _("Not consulted")),
            (_("Limited consultation"), _("Limited consultation")),
            (_("Free, Prior and Informed Consent (FPIC)"), _("Free, Prior and Informed Consent (FPIC)")),
            (_("Certified Free, Prior and Informed Consent (FPIC)"), _("Certified Free, Prior and Informed Consent (FPIC)")),
            (_("Other"), _("Other")),
        ), widget=forms.RadioSelect
    )
    tg_community_consultation_comment = forms.CharField(
        required=False, label=_("Additional comments"), widget=CommentInput
    )

    # How did community react?
    tg_community_reaction = TitleField(
        required=False, label="", initial=_("How did community react?")
    )
    community_reaction = forms.ChoiceField(
        required=False, label=_("Community reaction"), choices=(
            (10, _("Consent")),
            (20, _("Mixed reaction")),
            (30, _("Rejection")),
        ), widget=forms.RadioSelect
    )
    tg_community_reaction_comment = forms.CharField(
        required=False, label=_("Additional comments"), widget=CommentInput
    )

    # Land conflicts
    tg_land_conflicts = TitleField(
        required=False, label="", initial=_("Presence of land conflicts")
    )
    land_conflicts = forms.ChoiceField(
        required=False, label=_("Presence of land conflicts"), choices=(
            (10, _("Yes")),
            (20, _("No")),
        ), widget=forms.RadioSelect
    )
    tg_land_conflicts_comment = forms.CharField(
        required=False, label=_("Please specify details in Additional comments"),
        widget=CommentInput
    )

    # Displacement of people
    tg_displacement_of_people = TitleField(
        required=False, label="", initial=_("Displacement of people")
    )
    displacement_of_people = forms.ChoiceField(
        required=False, label=_("Displacement of people"), choices=(
            (10, _("Yes")),
            (20, _("No")),
        ), widget=forms.RadioSelect
    )
    number_of_displaced_people = forms.IntegerField(
        required=False, label=_("Number of people actually displaced"), widget=NumberInput
    )
    number_of_displaced_households = forms.IntegerField(
        required=False, label=_("Number of households actually displaced"), widget=NumberInput
    )
    number_of_people_displaced_from_community_land = forms.IntegerField(
        required=False, label=_("Number of people displaced out of their community land"),
        widget=NumberInput
    )
    number_of_people_displaced_within_community_land = forms.IntegerField(
        required=False, label=_("Number of people displaced staying on community land"),
        widget=NumberInput
    )
    number_of_people_displaced_from_fields = forms.IntegerField(
        required=False, label=_('Number of people displaced "only" from their agricultural fields'),
        widget=NumberInput
    )
    number_of_people_displaced_on_completion = forms.IntegerField(
        required=False,
        label=_('Number of people facing displacement once project is fully implemented'),
        widget=NumberInput
    )
    tg_number_of_displaced_people_comment = forms.CharField(
        required=False, label=_("Additional comments"), widget=CommentInput
    )

    tg_negative_impacts = TitleField(
        required=False, label="", initial=_("Negative impacts for local communities")
    )
    negative_impacts = forms.MultipleChoiceField(
        required=False, label=_("Negative impacts for local communities"), choices=(
            (10, _("Environmental degradation")),
            (20, _("Socio-economic")),
            (30, _("Cultural loss")),
            (40, _("Eviction")),
            (50, _("Displacement")),
            (60, _("Violence")),
            (70, _("Other")),
        ), widget=forms.CheckboxSelectMultiple
    )
    tg_negative_impacts_comment = forms.CharField(
        required=False, label=_("Please specify details in additional comments"),
        widget=CommentInput
    )

    # Promised compensation
    tg_promised_compensation = TitleField(
        required=False, label="", initial=_("Promised or received compensation")
    )
    promised_compensation = forms.CharField(
        required=False, label=_("Promised compensation (e.g. for damages or resettlements)"),
        widget=CommentInput
    )
    received_compensation = forms.CharField(
        required=False, label=_("Received compensation (e.g. for damages or resettlements)"),
        widget=CommentInput
    )

    # Promised benefits for local communities
    tg_promised_benefits = TitleField(
        required=False, label="", initial=_("Promised benefits for local communities")
    )
    promised_benefits = forms.MultipleChoiceField(
        required=False, label=_("Promised benefits for local communities"), choices=(
            (10, _("Health")),
            (20, _("Education")),
            (30, _("Productive infrastructure (e.g. irrigation, tractors, machinery...)")),
            (40, _("Roads")),
            (50, _("Capacity Building")),
            (60, _("Financial Support")),
            (70, _("Community shares in the investment project")),
            (80, _("Other")),
        ), widget=forms.CheckboxSelectMultiple
    )
    tg_promised_benefits_comment = forms.CharField(
        required=False, label=_("Please specify in additional comments"), widget=CommentInput
    )

    # Materialized benefits for local communities
    tg_materialized_benefits = TitleField(
        required=False, label="", initial=_("Materialized benefits for local communities")
    )
    materialized_benefits = forms.MultipleChoiceField(
        required=False, label=_("Materialized benefits for local communities"), choices=(
            (10, _("Health")),
            (20, _("Education")),
            (30, _("Productive infrastructure (e.g. irrigation, tractors, machinery...)")),
            (40, _("Roads")),
            (50, _("Capacity Building")),
            (60, _("Financial Support")),
            (70, _("Community shares in the investment project")),
            (80, _("Other")),
        ), widget=forms.CheckboxSelectMultiple
    )
    tg_materialized_benefits_comment = forms.CharField(
        required=False, label=_("Please specify in additional comments"), widget=CommentInput
    )

    # Presence of organizations and actions taken (e.g. farmer organizations, NGOs, etc.)
    tg_presence_of_organizations = TitleField(
        required=False,
        initial=_(
            "Presence of organizations and actions taken (e.g. farmer organizations, NGOs, etc.)"
        )
    )
    presence_of_organizations = forms.CharField(
        required=False,
        label=_(
            "Presence of organizations and actions taken (e.g. farmer organizations, NGOs, etc.)"
        ),
        widget=CommentInput
    )

    class Meta:
        name = 'local_communities'
