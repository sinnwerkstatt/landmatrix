from django.db.models import Q, QuerySet
from rest_framework import serializers

from apps.landmatrix.models.country import Country, Region

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
    DealWorkflowInfo2,
    InvestorWorkflowInfo2,
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


class RegionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Region
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
    operating_company = OperatingCompanySerializer(allow_null=True)

    @staticmethod
    def save_submodels(request, dv1: DealVersion2):
        # FIXME right now we're handling contracts, locations and datasources in the serializer. not very pretty
        # maybe drf-writable-nested would be an alternative

        location_nids = set()
        for location in request.data["version"].get("locations"):
            location_nids.add(location["nid"])
            Location.objects.update_or_create(
                nid=location["nid"],
                dealversion_id=dv1.id,
                defaults={
                    "name": location["name"],
                    "description": location["description"],
                    "point": location["point"],
                    "facility_name": location["facility_name"],
                    "level_of_accuracy": location["level_of_accuracy"],
                    "comment": location["comment"],
                },
            )
        Location.objects.filter(dealversion_id=dv1.id).exclude(
            nid__in=location_nids
        ).delete()

        contract_nids = set()
        for contract in request.data["version"].get("contracts"):
            contract_nids.add(contract["nid"])
            Contract.objects.update_or_create(
                nid=contract["nid"],
                dealversion_id=dv1.id,
                defaults={
                    "number": contract["number"],
                    "date": contract["date"],
                    "expiration_date": contract["expiration_date"],
                    "agreement_duration": contract["agreement_duration"],
                    "comment": contract["comment"],
                },
            )
        Contract.objects.filter(dealversion_id=dv1.id).exclude(
            nid__in=contract_nids
        ).delete()

        datasource_nids = set()
        for datasource in request.data["version"].get("datasources"):
            datasource_nids.add(datasource["nid"])
            DealDataSource.objects.update_or_create(
                nid=datasource["nid"],
                dealversion_id=dv1.id,
                defaults={
                    "type": datasource["type"],
                    "url": datasource["url"],
                    "file": datasource["file"],
                    "file_not_public": datasource["file_not_public"],
                    "publication_title": datasource["publication_title"],
                    "date": datasource["date"],
                    "name": datasource["name"],
                    "company": datasource["company"],
                    "email": datasource["email"],
                    "phone": datasource["phone"],
                    "includes_in_country_verified_information": datasource[
                        "includes_in_country_verified_information"
                    ],
                    "open_land_contracts_id": datasource["open_land_contracts_id"],
                    "comment": datasource["comment"],
                },
            )
        DealDataSource.objects.filter(dealversion_id=dv1.id).exclude(
            nid__in=datasource_nids
        ).delete()

    class Meta:
        model = DealVersion2
        fields = "__all__"


class Deal2Serializer(serializers.ModelSerializer):
    country = CountrySerializer()

    versions = DealVersionVersionsListSerializer(many=True)
    selected_version = DealVersionSerializer()
    workflowinfos = serializers.SerializerMethodField()

    @staticmethod
    def get_workflowinfos(obj: DealHull):
        return [
            x.to_dict()
            for x in DealWorkflowInfo2.objects.filter(deal_id=obj.id).order_by("-id")
        ]

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


class Investor2DealSerializer(serializers.ModelSerializer):
    class Meta:
        model = DealVersion2
        fields = ["id", "deal_id"]


class InvestorVersionSerializer(serializers.ModelSerializer):
    datasources = InvestorDataSourceSerializer(many=True, read_only=True)
    country = CountrySerializer()
    # deals = Investor2DealSerializer(many=True)
    deals = serializers.SerializerMethodField()

    @staticmethod
    def get_deals(obj: InvestorVersion2):
        target_deals = (
            DealHull.objects.filter(
                id__in=obj.dealversions.all().values_list("deal_id", flat=True)
            )
            .exclude(active_version=None)
            .prefetch_related("active_version")
        )

        return [
            {
                "id": d.id,
                "country": {"id": d.country_id} if d.country else None,
                "selected_version": {
                    "id": d.active_version.id,
                    "current_intention_of_investment": d.active_version.current_intention_of_investment,
                    "current_negotiation_status": d.active_version.current_negotiation_status,
                    "current_implementation_status": d.active_version.current_implementation_status,
                    "deal_size": d.active_version.deal_size,
                },
            }
            for d in target_deals
        ]

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

    @staticmethod
    def get_involvements(obj: InvestorHull):
        if hasattr(obj, "_selected_version_id"):
            return obj.versions.get(id=obj._selected_version_id).involvements_snapshot
        if obj.active_version:
            involvements: QuerySet[Involvement] = Involvement.objects.filter(
                Q(parent_investor_id=obj.id) | Q(child_investor_id=obj.id)
            )
            return [invo.to_dict(target_id=obj.id) for invo in involvements]
        else:
            # TODO should the draft version also have this involvements_snapshot?
            return obj.draft_version.involvements_snapshot

    # def get_deals(self):
    #     return

    @staticmethod
    def get_workflowinfos(obj: InvestorHull):
        return [
            x.to_new_dict()
            for x in InvestorWorkflowInfo2.objects.filter(investor_id=obj.id).order_by(
                "-id"
            )
        ]

    class Meta:
        model = InvestorHull
        fields = "__all__"
