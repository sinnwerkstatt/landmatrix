from django.db import models
from django.utils.translation import gettext as _
from nanoid import generate

from apps.landmatrix.models.fields import NanoIDField, LooseDateField
from apps.landmatrix.models.new import DealVersion


class Contract(models.Model):
    dealversion = models.ForeignKey(
        DealVersion, on_delete=models.CASCADE, related_name="contracts"
    )
    nid = NanoIDField("ID", max_length=15, db_index=True)
    number = models.CharField(_("Contract number"), blank=True)
    date = LooseDateField(_("Date"), blank=True, null=True)
    expiration_date = LooseDateField(_("Expiration date"), blank=True, null=True)
    agreement_duration = models.IntegerField(
        _("Duration of the agreement"), blank=True, null=True
    )
    comment = models.TextField(_("Comment"), blank=True)

    def to_dict(self):
        return {
            "nid": self.nid,
            "number": self.number,
            "date": self.date,
            "expiration_date": self.expiration_date,
            "agreement_duration": self.agreement_duration,
            "comment": self.comment,
        }

    def save(self, *args, **kwargs):
        if self._state.adding and not self.nid:
            self.nid = generate(size=8)
        super().save(*args, **kwargs)

    class Meta:
        unique_together = ["dealversion", "nid"]
        indexes = [models.Index(fields=["dealversion", "nid"])]
        ordering = ["id"]
