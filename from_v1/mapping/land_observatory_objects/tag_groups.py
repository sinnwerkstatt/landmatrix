from .tags import A_Tag, SH_Tag

from django.db import models
from django.contrib.gis.db import models as gismodels



class A_Tag_Group(models.Model):
    id = models.AutoField(primary_key=True)
    tg_id = models.IntegerField()
    fk_activity = models.IntegerField()
    fk_a_tag = models.IntegerField(blank=True, null=True)
    geometry = gismodels.GeometryField(srid=4326, spatial_index=True, dim=2)
    valid_from = models.DateTimeField()
    valid_to = models.DateTimeField()

    @property
    def tag(self):
        return A_Tag.objects.using('lo').get(pk=self.fk_a_tag)

    @property
    def tags(self):
        return A_Tag.objects.using('lo').filter(fk_a_tag_group=self.id)

    class Meta:
        app_label = 'from_v1'
        db_table = "a_tag_groups"

    def __str__(self):
        return "{} {} {} {} {}".format(self.id, self.tg_id, self.fk_activity, self.fk_a_tag, str(self.tags))


class SH_Tag_Group(models.Model):
    id = models.AutoField(primary_key=True)
    tg_id = models.IntegerField()
    fk_stakeholder = models.IntegerField()
    fk_sh_tag = models.IntegerField(blank=True, null=True)
    valid_from = models.DateTimeField()
    valid_to = models.DateTimeField()

    class Meta:
        app_label = 'from_v1'
        db_table = "sh_tag_groups"

    @property
    def tags(self):
        return SH_Tag.objects.using('lo').filter(fk_sh_tag_group=self.id)

    def __str__(self):
        return "{} {} {} {} {}".format(self.id, self.tg_id, self.fk_stakeholder, self.fk_sh_tag, str(self.tags))
