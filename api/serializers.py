__author__ = 'Lene Preuss <lp@sinnwerkstatt.com>'

from rest_framework import serializers
from landmatrix.models import Involvement, Activity, Stakeholder, PrimaryInvestor, Status, ActivityAttributeGroup

class InvolvementSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Involvement
        fields = ('url', 'id', 'investment_ratio', 'fk_activity', 'fk_stakeholder', 'fk_primary_investor')

class ActivitySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Activity
        fields = ('url', 'id', 'availability', 'fully_updated', 'fk_status')

class StakeholderSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Stakeholder
        fields = ('url', 'id', 'stakeholder_identifier', 'version', 'fk_status')

class PrimaryInvestorSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = PrimaryInvestor
        fields = ('url', 'id', 'name', 'fk_status')

class StatusSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Status
        fields = ('url', 'id', 'name', 'description')

class ActivityAttributeGroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ActivityAttributeGroup
        fields = ('url', 'id', 'fk_activity', 'name', 'date', 'attributes')