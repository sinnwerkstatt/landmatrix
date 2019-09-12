from django import forms


class ApproveRejectChangeForm(forms.Form):
    tg_action_comment = forms.CharField(
        required=True, label="", widget=forms.Textarea(attrs={'rows': '3'}))
