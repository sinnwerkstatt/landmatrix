
from django.db import models
from django.utils.translation import ugettext_lazy as _
from landmatrix.models.default_string_representation import DefaultStringRepresentation

class Language(DefaultStringRepresentation, models.Model):
    english_name = models.CharField(_("English name"), max_length=255)
    local_name = models.CharField(_("Local name"), max_length=255)
    locale = models.CharField(_("Locale"), max_length=31)
