from django.db import models
from wagtail.images import get_image_model_string
from wagtail.images.models import SourceImageIOError
from wagtailorderable.models import Orderable


class Partner(Orderable):
    name = models.CharField(max_length=500)
    logo = models.ForeignKey(
        get_image_model_string(),
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        verbose_name="Logo",
    )
    DONORS = "DONORS"
    PARTNERS = "PARTNERS"
    category = models.CharField(
        choices=[(DONORS, "Donors"), (PARTNERS, "Partners")], default=PARTNERS
    )
    homepage = models.URLField(blank=True)

    class Meta:
        verbose_name = "Partner"
        verbose_name_plural = "Partners"

    def __str__(self):
        return self.name

    def to_dict(self, rendition_str):
        try:
            logo = self.logo.get_rendition(rendition_str).url
        except (AttributeError, SourceImageIOError):
            logo = None
        return {
            "id": self.id,
            "name": self.name,
            "logo": logo,
            "category": self.category.title(),
            "homepage": self.homepage,
        }
