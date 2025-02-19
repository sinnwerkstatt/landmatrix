from rest_framework_dataclasses.serializers import DataclassSerializer

from rest_framework import serializers

from apps.landmatrix.models import DealQISnapshot, InvestorQISnapshot
from apps.landmatrix.quality_indicators import DEAL_QIS, INVESTOR_QIS
from apps.landmatrix.quality_indicators.dataclass import QualityIndicator, Subset
from apps.serializer import ReadOnlyModelSerializer


class QualityIndicatorSerializer(DataclassSerializer):
    class Meta:
        dataclass = QualityIndicator
        exclude = ("query",)


class QualityIndicatorSubsetSerializer(DataclassSerializer):
    class Meta:
        dataclass = Subset
        exclude = ("query",)


class QueryParamsSerializer(serializers.Serializer):
    inverse = serializers.BooleanField(required=False, default=False)


class DealQIDataSerializer(serializers.Serializer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for qi in DEAL_QIS:
            self.fields[qi.key] = serializers.IntegerField()

        self.fields["TOTAL"] = serializers.IntegerField()


class InvestorQIDataSerializer(serializers.Serializer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for qi in INVESTOR_QIS:
            self.fields[qi.key] = serializers.IntegerField()

        self.fields["TOTAL"] = serializers.IntegerField()


class DealQISnapshotSerializer(ReadOnlyModelSerializer):
    data = DealQIDataSerializer()
    # created_at = serializers.DateField(read_only=True)

    class Meta:
        model = DealQISnapshot
        fields = "__all__"


class InvestorQISnapshotSerializer(ReadOnlyModelSerializer):
    data = InvestorQIDataSerializer()
    # created_at = serializers.DateField(read_only=True)

    class Meta:
        model = InvestorQISnapshot
        fields = "__all__"
