__author__ = 'lene'

from rest_framework import serializers
from landmatrix.models import Involvement

class InvolvementSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Involvement
