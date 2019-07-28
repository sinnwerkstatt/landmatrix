from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.core.mail import EmailMessage, EmailMultiAlternatives
from django.template import loader
from django.utils import timezone

from .exceptions import NotificationError, AlreadySentError


class NotificationEmailManager(models.Manager):

    def send(self, *args, **kwargs):
        notification = NotificationEmail(*args, **kwargs)
        notification.send()

        return notification


class NotificationEmail(models.Model):
    """
    Notifications are saved to the database for debugging/forensics purposes.

    They can probably be deleted after not too long.

    The API is pretty simple: generally just use
    NotificationEmail.objects.send, with kwargs as follows:

        -   template_name: name of the template file (.html and .txt) to
            render
        -   context: a dictionary passed to the template for rendering
        -   to: comma separated string of email addresses
        -   cc: optional comma separated string of email addresses
        -   bcc: optional comma separated string of email addresses
        -   reply_to: optional comma separated string of email addresses
        -   from_email: optional from email address (if not provided,
            settings.DEFAULT_FROM_EMAIL is used)
        -   body_text: plain text body string
        -   body_html: optional HTML body string

    Exceptions are saved in the database and not raised.
    """
    STATUS_NEW = 1
    STATUS_SENT = 2
    STATUS_ERROR = 3

    STATUS_CHOICES = (
        (STATUS_NEW, _("New")),
        (STATUS_SENT, _("Sent")),
        (STATUS_ERROR, _("Error")),
    )

    created_on = models.DateTimeField(default=timezone.now,
                                      verbose_name=_("Created On"))
    sent_on = models.DateTimeField(blank=True, null=True, editable=False,
                                   verbose_name=_("Sent on"))
    sent_status = models.PositiveSmallIntegerField(choices=STATUS_CHOICES,
                                                   default=STATUS_NEW,
                                                   editable=False)
    sent_exception = models.TextField(blank=True)

    to = models.TextField(blank=False, verbose_name=_("To"))
    cc = models.TextField(blank=True, verbose_name=_("CC"))
    bcc = models.TextField(blank=True, verbose_name=_("BCC"))
    reply_to = models.TextField(blank=True, verbose_name=_("Reply To"))
    subject = models.CharField(max_length=255, blank=True,
                               verbose_name=_("Subject"))
    from_email = models.CharField(max_length=255, blank=True,
                                  verbose_name=_("From"))
    body_text = models.TextField(blank=False,
                                 verbose_name=_("Body Plain Text"))
    body_html = models.TextField(blank=True, verbose_name=_("Body HTML"))

    objects = NotificationEmailManager()

    class Meta:
        get_latest_by = 'created_on'

    def __init__(self, *args, template_name=None, context=None, **kwargs):
        super().__init__(*args, **kwargs)

        if template_name:
            self.render_template(template_name, context)

    def render_template(self, template_name, context):
        if not self.is_new:  # pragma: no cover
            raise NotificationError("Can't modify an existing email record.")

        text_template = loader.get_template('{}.txt'.format(template_name))
        html_template = loader.get_template('{}.html'.format(template_name))

        self.body_text = text_template.render(context)
        self.body_html = html_template.render(context)

    @property
    def is_sent(self):
        return self.sent_on and self.sent_status == self.STATUS_SENT or False

    @property
    def is_new(self):
        return (not self.sent_on) and self.sent_status == self.STATUS_NEW or False

    def send(self):
        if self.is_sent:
            raise AlreadySentError("Notification email has already been sent.")

        message_kwargs = {
            'subject': self.subject,
            'body': self.body_text,
            'from_email': self.from_email or None,
            'to': self.to.split(','),
        }
        if self.cc:
            message_kwargs['cc'] = self.cc.split(',')
        if self.bcc:
            message_kwargs['bcc'] = self.bcc.split(',')
        if self.reply_to:
            message_kwargs['reply_to'] = self.reply_to.split(',')

        if self.body_html:
            message = EmailMultiAlternatives(**message_kwargs)
            message.attach_alternative(self.body_html, 'text/html')
        else:
            message = EmailMessage(**message_kwargs)

        try:
            message.send()
        except Exception as err:  # pragma: no cover
            self.sent_status = self.STATUS_ERROR
            self.sent_exception = str(err)
        else:
            self.sent_status = self.STATUS_SENT
            self.sent_on = timezone.now()
            self.sent_exception = ''

        self.save()
