from django.conf import settings
from django.contrib.postgres.fields import JSONField
from django.db import models
from django.utils import timezone


class Version(models.Model):
    created_at = models.DateTimeField(db_index=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
    )
    serialized_data = JSONField()

    class Meta:
        abstract = True
        ordering = ["-pk"]

    def __str__(self):
        return f"#{self.object_id} v{self.id} @{self.created_at.date()}"

    def save(self, *args, **kwargs):
        if not self.pk and not self.created_at:
            self.created_at = timezone.now()
        super().save(*args, **kwargs)

    @classmethod
    def from_object(cls, obj, created_at=None, created_by=None):
        version, _ = cls.objects.get_or_create(
            created_at=created_at,
            created_by=created_by,
            object_id=obj.pk,
            serialized_data=obj.serialize_for_version(),
        )
        return version

    def enriched_dict(self) -> dict:
        edict = self.serialized_data
        edict["id"] = self.object_id
        for x in self.object._meta.fields:
            if x.__class__.__name__ == "ForeignKey":
                if edict.get(x.name):
                    edict[x.name] = x.related_model.objects.get(pk=edict[x.name])
        edict["created_at"] = self.created_at
        edict["created_by"] = self.created_by
        return edict


#     def retrieve_object(self):
#         obj = list(serializers.deserialize("json", json.dumps(self.serialized_data)))[0]
#         return obj.object

#     @classmethod
#     def create_from_obj(cls, obj, revision_id):
#         subclass = cls._get_current_subclass(obj)
#
#         serialized_json = serializers.serialize("json", (obj,))
#         serialized_fields = json.loads(serialized_json)
#
#         version = subclass(
#             revision_id=revision_id, object_id=obj.pk, serialized_data=serialized_fields
#         )
#         version.save()
#         return version
#
#
#     # TODO: Replace this ASAP with functools.cached_property (Python 3.8!)
#     @property
#     def fields(self):
#         fields = self.serialized_data[0]["fields"].copy()
#         fields["id"] = self.object_id
#         for field in self.model._meta.fields:
#             if fields.get(field.name) is None:
#                 continue
#             if isinstance(field, (DateTimeField, DateField)):
#                 content = fields[field.name]
#                 if isinstance(content, str):
#                     fields[field.name] = parser.parse(content)
#             elif isinstance(field, PointField):
#                 val = fields[field.name]
#                 srid, point = val.split(";", 1)
#                 x, y = point.replace("POINT (", "").replace(")", "").split(" ")
#                 srid = srid.replace("SRID=", "")
#                 fields[field.name] = Point(float(x), float(y), srid=srid)
#             elif isinstance(field, ForeignKey):
#                 fields[field.name] = field.related_model.objects.get(
#                     pk=fields[field.name]
#                 )
#         return fields
