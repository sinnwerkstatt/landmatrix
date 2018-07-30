from django.db import models


class Involvement(models.Model):
    id = models.AutoField(primary_key=True)
    fk_activity = models.IntegerField(null=False)
    fk_stakeholder = models.IntegerField(null=False)
    fk_stakeholder_role = models.IntegerField(null=False)

    class Meta:
        app_label = 'from_v1'
        db_table = "involvements"

    @property
    def role(self):
        return Stakeholder_Role.objects.using('lo').get(pk=self.fk_stakeholder_role)

    def __str__(self):
        return "{}: {} ({})".format(self.fk_activity, self.fk_stakeholder, self.role.name)


class Stakeholder_Role(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField()

    class Meta:
        app_label = 'from_v1'
        db_table = "stakeholder_roles"
