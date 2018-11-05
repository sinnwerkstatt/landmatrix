from django.db import models
from django.contrib.gis.db import models as gismodels

from .tag_groups import A_Tag_Group


class Activity(models.Model):
    id = models.AutoField(primary_key=True)
    activity_identifier = models.CharField(max_length=255, null=False)
    fk_changeset = models.IntegerField()
    point = gismodels.GeometryField(srid=4326, spatial_index=True, dim=2)
    fk_status = models.IntegerField()
    version = models.IntegerField()
    reliability = models.IntegerField()
    previous_version = models.IntegerField()
    timestamp_entry = models.DateTimeField()
    fk_user_review = models.IntegerField()
    timestamp_review = models.DateTimeField()
    comment_review = models.CharField(max_length=255)
    fk_profile = models.IntegerField()

    class Meta:
        app_label = 'from_v1'
        db_table = "activities"

    @property
    def identifier(self):
        return self.activity_identifier

    @property
    def tag_groups(self):
        return A_Tag_Group.objects.using('lo').filter(fk_activity=self.id)

    def __str__(self):
        """
        if self.point is None:
            geom = '-'
        else:
            geom = wkb.loads(str(self.point.geom_wkb)).wkt
        """
        geom = '***'
        return (
            '<Activity> id [ %s ] | activity_identifier [ %s ] | fk_changeset '
            '[ %s ] | point [ %s ] | fk_status [ %s ] | version [ %s ] | '
            'previous_version [ %s ] | fk_user_review [ %s ] | '
            'timestamp_review [ %s ] | comment_review [ %s ] | fk_profile [ %s'
            ' ]' % (
                self.id, self.activity_identifier, self.fk_changeset, geom,
                self.fk_status, self.version, self.previous_version,
                self.fk_user_review, self.timestamp_review,
                self.comment_review, self.fk_profile))

    def get_comments(self):
        return DBSession.query(Comment).\
            filter(Comment.activity_identifier == self.activity_identifier).\
            all()

