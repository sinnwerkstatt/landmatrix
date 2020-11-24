import json

from dateutil import parser
from django.conf import settings
from django.contrib.gis.db.models import PointField
from django.contrib.postgres.fields import JSONField, ArrayField
from django.db import models
from django.db.models import DateTimeField, DateField, ForeignKey
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.core import serializers
from django.contrib.gis.geos import Point


class Revision(models.Model):
    date_created = models.DateTimeField(
        db_index=True,
        verbose_name=_("date created"),
        help_text="The date and time this revision was created.",
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        verbose_name=_("user"),
        help_text="The user who created this revision.",
    )

    comment = models.TextField(
        blank=True,
        verbose_name=_("comment"),
        help_text="A text comment on this revision.",
    )

    def save(self, *args, **kwargs):
        if not self.pk and not self.date_created:
            self.date_created = timezone.now()
        super().save(*args, **kwargs)


class Version(models.Model):
    model = None

    revision = models.ForeignKey(
        Revision,
        on_delete=models.CASCADE,
        help_text="The revision that contains this version.",
    )
    object_id = models.IntegerField(null=True, blank=True)
    serialized_data = JSONField()

    class Meta:
        abstract = True
        ordering = ["-pk"]

    def __str__(self):
        return f"{self.object_id}"

    @classmethod
    def _get_current_subclass(cls, obj):
        subclasses = [s for s in cls.__subclasses__() if s.model == obj.__class__]
        if not subclasses:
            raise Exception(f"Can not find correct Version-model for {obj}")
        if len(subclasses) > 1:
            raise Exception("You must've accidentally registered too many subclasses")
        return subclasses[0]

    @classmethod
    def create_from_obj(cls, obj, revision):
        subclass = cls._get_current_subclass(obj)

        serialized_json = serializers.serialize("json", (obj,))
        serialized_fields = json.loads(serialized_json)

        version = subclass(
            revision=revision, object_id=obj.pk, serialized_data=serialized_fields
        )
        version.save()
        return version

    def retrieve_object(self):
        obj = list(serializers.deserialize("json", json.dumps(self.serialized_data)))[0]
        return obj.object

    # TODO: Replace this ASAP with functools.cached_property (Python 3.8!)
    @property
    def fields(self):
        fields = self.serialized_data[0]["fields"]
        fields["id"] = self.object_id
        for field in self.model._meta.fields:
            if fields[field.name] is None:
                continue
            if isinstance(field, (DateTimeField, DateField)):
                content = fields[field.name]
                if isinstance(content, str):
                    fields[field.name] = parser.parse(content)
            elif isinstance(field, PointField):
                val = fields[field.name]
                srid, point = val.split(";", 1)
                x, y = point.replace("POINT (", "").replace(")", "").split(" ")
                srid = srid.replace("SRID=", "")
                fields[field.name] = Point(float(x), float(y), srid=srid)
            elif isinstance(field, ForeignKey):
                fields[field.name] = field.related_model.objects.get(
                    pk=fields[field.name]
                )
        return fields
