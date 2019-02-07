from django.db import models
from django.utils.translation import ugettext_lazy as _

from .managers import MessageManager


class Message(models.Model):

    LEVEL_DEBUG = 'debug'
    LEVEL_INFO = 'info'
    LEVEL_SUCCESS = 'success'
    LEVEL_WARNING = 'warning'
    LEVEL_ERROR = 'error'
    LEVEL_CHOICES = (
        (LEVEL_DEBUG, _('Debug')),
        (LEVEL_INFO, _('Info')),
        (LEVEL_SUCCESS, _('Success')),
        (LEVEL_WARNING, _('Warning')),
        (LEVEL_ERROR, _('Error')),
    )

    title = models.CharField(_('Title'), max_length=255, blank=True, null=True)
    text = models.TextField(_('Text'))
    level = models.CharField(_('Level'), max_length=10, choices=LEVEL_CHOICES, default=LEVEL_INFO)

    is_active = models.BooleanField(_('Is active'))

    objects = MessageManager()

    class Meta:
        verbose_name = _('Message')
        verbose_name_plural = _('Messages')
