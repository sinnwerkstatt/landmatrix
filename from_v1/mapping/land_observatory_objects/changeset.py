from django.db import models



class Changeset(models.Model):
    id = models.AutoField(primary_key=True)
    fk_user = models.IntegerField(null=False)
    timestamp = models.DateTimeField(null=False)
    source = models.TextField("source")
    diff = models.TextField("diff")

    class Meta:
        app_label = 'from_v1'
        db_table = "changesets"

