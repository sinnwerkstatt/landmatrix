__author__ = 'Lene Preuss <lp@sinnwerkstatt.com>'

from django import forms


class UserModelChoiceField(forms.ModelChoiceField):
    """
    Extend ModelChoiceField for users so that the choices are
    listed as 'first_name last_name (username)' instead of just
    'username'.

    """
    def label_from_instance(self, obj):
        return "%s" % obj.get_full_name() or obj.username

