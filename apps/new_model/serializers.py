from django.db.models import Q, QuerySet
from rest_framework import serializers

from apps.landmatrix.models.country import Country
from apps.landmatrix.models.investor import InvestorWorkflowInfo
from apps.new_model.models import (
    DealVersion2,
    DealHull,
    Location,
    DealDataSource,
    Contract,
    Area,
    InvestorHull,
    InvestorVersion2,
    InvestorDataSource,
    Involvement,
)


class DealVersionVersionsListSerializer(serializers.ModelSerializer):
    class Meta:
        model = DealVersion2
        fields = [
            "id",
            "created_at",
            "created_by_id",
            "sent_to_review_at",
            "sent_to_review_by_id",
            "reviewed_at",
            "reviewed_by_id",
            "activated_at",
            "activated_by_id",
            "fully_updated",
            "status",
        ]


class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = ["id", "name"]


class LocationAreaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Area
        fields = "__all__"


class LocationSerializer(serializers.ModelSerializer):
    areas = LocationAreaSerializer(many=True, read_only=True)

    class Meta:
        model = Location
        fields = "__all__"


class DealDataSourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = DealDataSource
        fields = "__all__"


class ContractSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contract
        fields = "__all__"


class OperatingCompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = InvestorVersion2
        fields = "__all__"


class DealVersionSerializer(serializers.ModelSerializer):
    locations = LocationSerializer(many=True, read_only=True)
    contracts = ContractSerializer(many=True, read_only=True)
    datasources = DealDataSourceSerializer(many=True, read_only=True)
    operating_company = OperatingCompanySerializer()

    class Meta:
        model = DealVersion2
        fields = "__all__"


class Deal2Serializer(serializers.ModelSerializer):
    country = CountrySerializer()
    versions = DealVersionVersionsListSerializer(many=True)
    selected_version = DealVersionSerializer()

    class Meta:
        model = DealHull
        fields = "__all__"


class InvestorVersionVersionsListSerializer(serializers.ModelSerializer):
    class Meta:
        model = InvestorVersion2
        fields = [
            "id",
            "created_at",
            "created_by_id",
            "sent_to_review_at",
            "sent_to_review_by_id",
            "reviewed_at",
            "reviewed_by_id",
            "activated_at",
            "activated_by_id",
            "status",
        ]


class InvestorDataSourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = InvestorDataSource
        fields = "__all__"


class InvestorVersionSerializer(serializers.ModelSerializer):
    datasources = InvestorDataSourceSerializer(many=True, read_only=True)
    country = CountrySerializer()

    class Meta:
        model = InvestorVersion2
        fields = "__all__"


# class InvolvementSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Involvement
#         fields = "__all__"


class Investor2Serializer(serializers.ModelSerializer):
    versions = InvestorVersionVersionsListSerializer(many=True)
    selected_version = InvestorVersionSerializer()
    # involvements = InvolvementSerializer(many=True)
    involvements = serializers.SerializerMethodField()
    workflowinfos = serializers.SerializerMethodField()

    class Meta:
        model = InvestorHull
        fields = "__all__"

    @staticmethod
    def get_involvements(obj: InvestorHull):
        if hasattr(obj, "_selected_version_id"):
            return obj.versions.get(id=obj._selected_version_id).involvements_snapshot
        if obj.active_version:
            involvements: QuerySet[Involvement] = Involvement.objects.filter(
                Q(parent_investor_id=obj.id) | Q(child_investor_id=obj.id)
            )
            return [invo.to_dict() for invo in involvements]
        else:
            # TODO should the draft version also have this involvements_snapshot?
            return obj.draft_version.involvements_snapshot

    @staticmethod
    def get_workflowinfos(obj: InvestorHull):
        return [
            x.to_new_dict()
            for x in InvestorWorkflowInfo.objects.filter(investor_id=obj.id).order_by(
                "-id"
            )
        ]
