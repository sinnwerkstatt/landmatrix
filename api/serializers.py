__author__ = 'Lene Preuss <lp@sinnwerkstatt.com>'

from rest_framework import serializers
from landmatrix.models import Involvement, Activity, Stakeholder, PrimaryInvestor, Status

class InvolvementSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Involvement
        fields = ('url', 'investment_ratio', 'fk_activity', 'fk_stakeholder', 'fk_primary_investor')

class ActivitySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Activity
        fields = ('url', 'availability', 'fully_updated', 'fk_status')

class StakeholderSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Stakeholder
        fields = ('url', 'stakeholder_identifier', 'version', 'fk_status')

class PrimaryInvestorSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = PrimaryInvestor
        fields = ('url', 'name', 'fk_status')

class StatusSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Status
        fields = ('url', 'name', 'description')
