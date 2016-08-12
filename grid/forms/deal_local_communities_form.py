from django import forms
from django.utils.translation import ugettext_lazy as _

from grid.forms.base_form import BaseForm
from grid.widgets import TitleField, CommentInput, NumberInput, MultiCharField


__author__ = 'Lene Preuss <lp@sinnwerkstatt.com>'


class DealLocalCommunitiesForm(BaseForm):
    RECOGNITION_STATUS_CHOICES = (
        (
            "Indigenous Peoples traditional or customary rights recognized by government",
            _("Indigenous Peoples traditional or customary rights recognized by government")
        ),
        (
            "Indigenous Peoples traditional or customary rights not recognized by government",
            _("Indigenous Peoples traditional or customary rights not recognized by government")
        ),
        (
            "Community traditional or customary rights recognized by government",
            _("Community traditional or customary rights recognized by government")
        ),
        (
            "Community traditional or customary rights not recognized by government",
            _("Community traditional or customary rights not recognized by government")
        ),
    )
    COMMUNITY_CONSULTATION_CHOICES = (
        ("Not consulted", _("Not consulted")),
        ("Limited consultation", _("Limited consultation")),
        (
            "Free, Prior and Informed Consent (FPIC)",
            _("Free, Prior and Informed Consent (FPIC)")
        ),
        (
            "Certified Free, Prior and Informed Consent (FPIC)",
            _("Certified Free, Prior and Informed Consent (FPIC)")
        ),
        ("Other", _("Other")),
    )
    COMMUNITY_REACTION_CHOICES = (
        ("Consent", _("Consent")),
        ("Mixed reaction", _("Mixed reaction")),
        ("Rejection", _("Rejection")),
    )
    # TODO: convert to booleanfield?
    BOOLEAN_CHOICES = (
        ("Yes", _("Yes")),
        ("No", _("No")),
    )
    NEGATIVE_IMPACTS_CHOICES = (
        ("Environmental degradation", _("Environmental degradation")),
        ("Socio-economic", _("Socio-economic")),
        ("Cultural loss", _("Cultural loss")),
        ("Eviction", _("Eviction")),
        ("Displacement", _("Displacement")),
        ("Violence", _("Violence")),
        ("Other", _("Other")),
    )
    BENEFITS_CHOICES = (
        ("Health", _("Health")),
        ("Education", _("Education")),
        (
            "Productive infrastructure",
            _("Productive infrastructure (e.g. irrigation, tractors, machinery...)")
        ),
        ("Roads", _("Roads")),
        ("Capacity Building", _("Capacity Building")),
        ("Financial Support", _("Financial Support")),
        (
            "Community shares in the investment project",
            _("Community shares in the investment project")
        ),
        ("Other", _("Other")),
    )

    form_title = _('Local communities / indigenous peoples')

    # Names of affected communities and indigenous peoples
    tg_names_of_affected = TitleField(
        required=False, label="",
        initial=_("Names of communities / indigenous peoples affected"))
    name_of_community = MultiCharField(
        required=False, label=_("Name of community"), widget=forms.TextInput)
    name_of_indigenous_people = MultiCharField(
        required=False, label=_("Name of indigenous people"),
        widget=forms.TextInput)
    tg_affected_comment = forms.CharField(
        required=False, label=_("Comment on Names of affected people"),
        widget=CommentInput)

    # Recognitions status of community land tenure
    tg_recognition_status = TitleField(
        required=False, label="",
        initial=_("Recognitions status of community land tenure"))
    recognition_status = forms.MultipleChoiceField(
        required=False, label=_("Recognition status of community land tenure"),
        choices=RECOGNITION_STATUS_CHOICES,
        widget=forms.CheckboxSelectMultiple)
    tg_recognition_status_comment = forms.CharField(
        required=False,
        label=_("Comment on Recognitions status of community land tenure"),
        widget=CommentInput)

    # Consultation of local community
    tg_community_consultation = TitleField(
        required=False, label="", initial=_("Consultation of local community"))
    community_consultation = forms.ChoiceField(
        required=False, label=_("Community consultation"),
        choices=COMMUNITY_CONSULTATION_CHOICES, widget=forms.RadioSelect)
    tg_community_consultation_comment = forms.CharField(
        required=False,
        label=_("Comment on Consultation of local community"),
        widget=CommentInput)

    # How did community react?
    tg_community_reaction = TitleField(
        required=False, label="", initial=_("How did the community react?"))
    community_reaction = forms.ChoiceField(
        required=False, label=_("Community reaction"),
        choices=COMMUNITY_REACTION_CHOICES, widget=forms.RadioSelect)
    tg_community_reaction_comment = forms.CharField(
        required=False, label=_("Comment on Community reaction"),
        widget=CommentInput)

    # Land conflicts
    tg_land_conflicts = TitleField(
        required=False, label="", initial=_("Presence of land conflicts"))
    land_conflicts = forms.ChoiceField(
        required=False, label=_("Presence of land conflicts"),
        choices=BOOLEAN_CHOICES, widget=forms.RadioSelect)
    tg_land_conflicts_comment = forms.CharField(
        required=False, label=_("Comment on Presence of land conflicts"),
        widget=CommentInput)

    # Displacement of people
    tg_displacement_of_people = TitleField(
        required=False, label="", initial=_("Displacement of people")
    )
    displacement_of_people = forms.ChoiceField(
        required=False, label=_("Displacement of people"),
        choices=BOOLEAN_CHOICES, widget=forms.RadioSelect)
    number_of_displaced_people = forms.IntegerField(
        required=False, label=_("Number of people actually displaced"),
        widget=NumberInput)
    number_of_displaced_households = forms.IntegerField(
        required=False, label=_("Number of households actually displaced"),
        widget=NumberInput)
    number_of_people_displaced_from_community_land = forms.IntegerField(
        required=False,
        label=_("Number of people displaced out of their community land"),
        widget=NumberInput)
    number_of_people_displaced_within_community_land = forms.IntegerField(
        required=False,
        label=_("Number of people displaced staying on community land"),
        widget=NumberInput)
    number_of_households_displaced_from_fields = forms.IntegerField(
        required=False,
        label=_('Number of households displaced "only" from their agricultural fields'),
        widget=NumberInput)
    number_of_people_displaced_on_completion = forms.IntegerField(
        required=False,
        label=_('Number of people facing displacement once project is fully implemented'),
        widget=NumberInput)
    tg_number_of_displaced_people_comment = forms.CharField(
        required=False, label=_("Comment on Displacement of people"),
        widget=CommentInput)

    tg_negative_impacts = TitleField(
        required=False, label="",
        initial=_("Negative impacts for local communities"))
    negative_impacts = forms.MultipleChoiceField(
        required=False, label=_("Negative impacts for local communities"),
        choices=NEGATIVE_IMPACTS_CHOICES, widget=forms.CheckboxSelectMultiple)
    tg_negative_impacts_comment = forms.CharField(
        required=False,
        label=_("Comment on Negative impacts for local communities"),
        widget=CommentInput)

    # Promised compensation
    tg_promised_compensation = TitleField(
        required=False, label="",
        initial=_("Promised or received compensation"))
    promised_compensation = forms.CharField(
        required=False,
        label=_("Promised compensation (e.g. for damages or resettlements)"),
        widget=CommentInput)
    received_compensation = forms.CharField(
        required=False,
        label=_("Received compensation (e.g. for damages or resettlements)"),
        widget=CommentInput)

    # Promised benefits for local communities
    tg_promised_benefits = TitleField(
        required=False, label="",
        initial=_("Promised benefits for local communities"))
    promised_benefits = forms.MultipleChoiceField(
        required=False, label=_("Promised benefits for local communities"),
        choices=BENEFITS_CHOICES, widget=forms.CheckboxSelectMultiple)
    tg_promised_benefits_comment = forms.CharField(
        required=False,
        label=_("Comment on Promised benefits for local communities"),
        widget=CommentInput)

    # Materialized benefits for local communities
    tg_materialized_benefits = TitleField(
        required=False, label="",
        initial=_("Materialized benefits for local communities")
    )
    materialized_benefits = forms.MultipleChoiceField(
        required=False, label=_("Materialized benefits for local communities"),
        choices=BENEFITS_CHOICES, widget=forms.CheckboxSelectMultiple)
    tg_materialized_benefits_comment = forms.CharField(
        required=False,
        label=_("Comment on Materialized benefits for local communities"),
        widget=CommentInput)

    # Presence of organizations and actions taken (e.g. farmer organizations, NGOs, etc.)
    tg_presence_of_organizations = TitleField(
        required=False,
        initial=_("Presence of organizations and actions taken (e.g. farmer organizations, NGOs, etc.)"))
    presence_of_organizations = forms.CharField(
        required=False,
        label=_("Presence of organizations and actions taken (e.g. farmer organizations, NGOs, etc.)"),
        widget=CommentInput)

    class Meta:
        name = 'local_communities'
