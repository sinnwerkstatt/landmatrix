from django import forms
from django.forms.utils import ErrorDict
from threadedcomments import get_form as get_threaded_comment_form
from captcha.fields import ReCaptchaField

from .models import ThreadedComment


ThreadedCommentForm = get_threaded_comment_form()


class PublicCommentForm(ThreadedCommentForm):

    spam_protection = ReCaptchaField()
    url = forms.CharField(required=False, widget=forms.HiddenInput)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Don't bother with honeypot field, we've got recaptcha
        del self.fields['honeypot']

    def security_errors(self):
        '''
        Include the reCAPTCHA field in security errors.
        '''
        errors = ErrorDict()
        for field_name in ['spam_protection', 'timestamp', 'security_hash']:
            if field_name in self.errors:
                errors[field_name] = self.errors[field_name]

        return errors


class EditCommentForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        '''
        Display a couple fields as readonly (easier than customizing the
        template).
        '''
        super().__init__(*args, **kwargs)
        for readonly_field in EditCommentForm.Meta.readonly_fields:
            self.fields[readonly_field].widget.attrs['readonly'] = True

    class Meta:
        model = ThreadedComment
        fields = (
            'user_name', 'user_email', 'title', 'comment', 'ip_address',
            'is_public', 'is_removed',
        )
        readonly_fields = ('user_name', 'user_email', 'ip_address',)
