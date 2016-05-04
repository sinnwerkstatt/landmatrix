from django.forms.utils import ErrorDict
from threadedcomments import get_form as get_threaded_comment_form
from captcha.fields import ReCaptchaField


ThreadedCommentForm = get_threaded_comment_form()


class PublicCommentForm(ThreadedCommentForm):

    spam_protection = ReCaptchaField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Don't bother with honeypot field, we've got recaptcha
        self.fields.pop('honeypot')

    def security_errors(self):
        '''
        Include the reCAPTCHA field in security errors.
        '''
        errors = ErrorDict()
        for field_name in ['spam_protection', 'timestamp', 'security_hash']:
            if field_name in self.errors:
                errors[field_name] = self.errors[field_name]

        return errors
