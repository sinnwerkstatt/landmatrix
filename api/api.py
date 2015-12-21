from landmatrix.models import Activity, Status, ActivityAttributeGroup

from tastypie import fields
from tastypie.resources import ModelResource

__author__ = 'Lene Preuss <lp@sinnwerkstatt.com>'


class StatusResource(ModelResource):
    class Meta:
        queryset = Status.objects.all()


class ActivityResource(ModelResource):
    fk_status = fields.ForeignKey(StatusResource, attribute='fk_status')
    class Meta:
        queryset = Activity.objects.all()


class ActivityAttributeGroupResource(ModelResource):
    fk_activity = fields.ForeignKey(ActivityResource, attribute='fk_activity')
    class Meta:
        queryset = ActivityAttributeGroup.objects.all()
