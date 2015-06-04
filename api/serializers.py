__author__ = 'Lene Preuss <lp@sinnwerkstatt.com>'

from rest_framework import serializers
from landmatrix.models import Involvement

class InvolvementSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Involvement
