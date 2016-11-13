from django.db import models
from django.utils.translation import ugettext_lazy as _



class BrowseRule(models.Model):
    name = models.CharField(_("Name"), max_length=255)
    rule_type = models.CharField(_("Rule type"), max_length=255, choices=(
        ('browse','Browse rule'),
        ('generic','Generic rule')
    ))

    def __str__(self):
        return self.name

