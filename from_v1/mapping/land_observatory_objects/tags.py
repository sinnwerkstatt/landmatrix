from django.db import models

__author__ = 'Lene Preuss <lp@sinnwerkstatt.com>'


class A_Tag(models.Model):
    id = models.AutoField(primary_key=True)
    fk_a_tag_group = models.IntegerField()
    fk_a_key = models.IntegerField()
    fk_a_value = models.IntegerField()

    @property
    def key(self):
        return A_Key.objects.using('lo').get(id=self.fk_a_key)

    @property
    def value(self):
        return A_Value.objects.using('lo').get(id=self.fk_a_value)

    class Meta:
        db_table = "a_tags"

    def __str__(self):
        return self.key.key + ' => ' + self.value.value


class A_Key(models.Model):
    id = models.AutoField(primary_key=True)
    fk_a_key = models.ForeignKey("A_Key", db_column="fk_a_key", blank=True, null=True)
    fk_language = models.IntegerField(blank=True, null=True)
    key = models.CharField("Key", max_length=255)
    type = models.CharField("Type", max_length=255)
    helptext = models.TextField("helptext")
    description = models.TextField("description")
    validator = models.TextField("validator")

    class Meta:
        db_table = "a_keys"


class A_Value(models.Model):
    id = models.AutoField(primary_key=True)
    fk_a_value = models.ForeignKey("A_Value", db_column="fk_a_value", blank=True, null=True)
    fk_language = models.IntegerField(blank=True, null=True)
    value = models.TextField("helptext")
    fk_a_key = models.ForeignKey("A_Key", db_column="fk_a_key", blank=True, null=True)
    order = models.IntegerField(blank=True, null=True)

    class Meta:
        db_table = "a_values"
