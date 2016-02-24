__author__ = 'Lene Preuss <lp@sinnwerkstatt.com>'

from grid.forms.base_form import BaseForm
from grid.widgets import TitleField, CommentInput, NumberInput

from django import forms
from django.utils.translation import ugettext_lazy as _


class DealLocalCommunitiesForm(BaseForm):

    form_title = _('Local communities')

    # How did community react?
    tg_community_reaction = TitleField(required=False, label="", initial=_("How did community react?"))
    community_reaction = forms.ChoiceField(required=False, label=_("Community reaction"), choices=(
        (10, _("Consent")),
        (20, _("Mixed reaction")),
        (30, _("Rejection")),
    ), widget=forms.RadioSelect)
    tg_community_reaction_comment = forms.CharField(required=False, label=_("Additional comments"), widget=CommentInput)
    # Consultation of local community
    tg_community_consultation = TitleField(required=False, label="", initial=_("Consultation of local community"))
    community_consultation = forms.ChoiceField(required=False, label=_("Community consultation"), choices=(
        (10, _("Not consulted")),
        (20, _("Limited consultation")),
        (30, _("Free prior and informed consent")),
        (40, _("Other")),
    ), widget=forms.RadioSelect)
    tg_community_consultation_comment = forms.CharField(required=False, label=_("Additional comments"), widget=CommentInput)
    # Promised or received compensation
    tg_community_compensation = TitleField(required=False, label="", initial=_("Promised or received compensation"))
    community_compensation = forms.CharField(required=False, label=_("Community compensation"), widget=CommentInput)
    # Benefits for local communities
    tg_community_benefits = TitleField(required=False, label="", initial=_("Benefits for local communities"))
    community_benefits = forms.MultipleChoiceField(required=False, label=_("Community benefits"), choices=(
        (10, _("Health")),
        (20, _("Education")),
        (30, _("Productive infrastructure (e.g. irrigation, tractors, machinery...)")),
        (40, _("Roads")),
        (50, _("Capacity Building")),
        (60, _("Financial Support")),
        (70, _("Other")),
    ), widget=forms.CheckboxSelectMultiple)
    tg_community_benefits_comment = forms.CharField(required=False, label=_("Additional comments"), widget=CommentInput)
    # Number of people actually displaced
    tg_number_of_displaced_people = TitleField(required=False, label="", initial=_("Number of people actually displaced"))
    number_of_displaced_people = forms.IntegerField(required=False, label=_("Number of displaced people"), help_text="", widget=NumberInput)
    tg_number_of_displaced_people_comment = forms.CharField(required=False, label=_("Additional comments"), widget=CommentInput)
