__author__ = 'Lene Preuss <lp@sinnwerkstatt.com>'

from tastypie.resources import ModelResource
from landmatrix.models import Involvement, Activity, Stakeholder, PrimaryInvestor, Status, ActivityAttributeGroup

class InvolvementResource(ModelResource):
    class Meta:
        queryset = Involvement.objects.all()
        fields = ('url', 'id', 'investment_ratio', 'fk_activity', 'fk_stakeholder', 'fk_primary_investor')

class ActivityResource(ModelResource):
    class Meta:
        queryset = Activity.objects.all()
        fields = ('url', 'id', 'availability', 'fully_updated', 'fk_status')

class StakeholderResource(ModelResource):
    class Meta:
        queryset = Stakeholder.objects.all()
        fields = ('url', 'id', 'stakeholder_identifier', 'version', 'fk_status')

class PrimaryInvestorResource(ModelResource):
    class Meta:
        queryset = PrimaryInvestor.objects.all()
        fields = ('url', 'id', 'name', 'fk_status')

class ActivityAttributeGroupResource(ModelResource):
    class Meta:
        queryset = ActivityAttributeGroup.objects.all()
        fields = ('url', 'id', 'fk_activity', 'name', 'date', 'attributes')

class StatusResource(ModelResource):
    class Meta:
        queryset = Status.objects.all()
