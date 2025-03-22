from django.contrib.gis.geos import GEOSGeometry
from django.db.models.query_utils import Q
from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers

from apps.accounts.models import User
from apps.landmatrix.models.abstract import VersionStatus
from apps.landmatrix.models.context_help import ContextHelp
from apps.landmatrix.models.country import Country, Region
from apps.landmatrix.models.currency import Currency
from apps.landmatrix.models.deal import (
    Area,
    Contract,
    DealDataSource,
    DealHull,
    DealVersion,
    DealWorkflowInfo,
    Location,
)
from apps.landmatrix.models.investor import (
    InvestorDataSource,
    InvestorHull,
    InvestorVersion,
    InvestorWorkflowInfo,
    Involvement,
)
from apps.landmatrix.permissions import is_editor_or_higher, is_reporter_or_higher
from apps.serializer import ReadOnlyModelSerializer
from django_pydantic_jsonfield import PydanticJSONFieldMixin


class CurrencySerializer(serializers.ModelSerializer):
    class Meta:
        model = Currency
        fields = ["id", "code", "name", "symbol"]


class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = [
            "id",
            "name",
            # "slug",
            "high_income",
            "code_alpha2",
            "point_lat",
            "point_lon",
            "point_lat_min",
            "point_lon_min",
            "point_lat_max",
            "point_lon_max",
            "observatory_page_id",
            "region_id",
            "deals",
        ]


class RegionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Region
        fields = [
            "id",
            "name",
            # "slug",
            "observatory_page_id",
            "point_lat_min",
            "point_lon_min",
            "point_lat_max",
            "point_lon_max",
        ]


class DealVersionVersionsListSerializer(ReadOnlyModelSerializer):
    class Meta:
        model = DealVersion
        fields = [
            "id",
            "created_at",
            "created_by_id",
            "modified_at",
            "modified_by_id",
            "sent_to_review_at",
            "sent_to_review_by_id",
            "sent_to_activation_at",
            "sent_to_activation_by_id",
            "activated_at",
            "activated_by_id",
            "status",
            "fully_updated",
            "is_public",
        ]


class LocationAreaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Area
        # fields = "__all__"
        exclude = ("location",)


class LocationSerializer(serializers.ModelSerializer):
    areas = LocationAreaSerializer(many=True, read_only=True)

    class Meta:
        model = Location
        fields = "__all__"


class _BaseDataSourceSerializer(serializers.ModelSerializer):
    file = serializers.SerializerMethodField()

    @staticmethod
    def get_file(obj: DealDataSource) -> str | None:
        return obj.file.name if obj.file else None


class DealDataSourceSerializer(_BaseDataSourceSerializer):
    class Meta:
        model = DealDataSource
        fields = "__all__"


class ContractSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contract
        fields = "__all__"


class MyModelSerializer(PydanticJSONFieldMixin, serializers.ModelSerializer):
    class Meta:
        abstract = True


class DealVersionSerializer(MyModelSerializer):
    locations = LocationSerializer(many=True, read_only=True)
    contracts = ContractSerializer(many=True, read_only=True)
    datasources = DealDataSourceSerializer(many=True, read_only=True)
    operating_company_id = serializers.PrimaryKeyRelatedField[InvestorHull](
        read_only=True
    )

    # creating these because DRF shows these fields as "created_by", instead of "~_id"
    created_by_id = serializers.PrimaryKeyRelatedField[User](read_only=True)
    modified_by_id = serializers.PrimaryKeyRelatedField[User](read_only=True)
    sent_to_review_by_id = serializers.PrimaryKeyRelatedField[User](read_only=True)
    sent_to_activation_by_id = serializers.PrimaryKeyRelatedField[User](read_only=True)
    activated_by_id = serializers.PrimaryKeyRelatedField[User](read_only=True)

    class Meta:
        model = DealVersion
        read_only_fields = (
            "id",
            "deal",
            # calculated
            "is_public",
            "has_known_investor",
            "parent_companies",
            "top_investors",
            "current_contract_size",
            "current_production_size",
            "current_intention_of_investment",
            "current_negotiation_status",
            "current_implementation_status",
            "current_crops",
            "current_animals",
            "current_mineral_resources",
            "current_electricity_generation",
            "current_carbon_sequestration",
            "deal_size",
            "initiation_year",
            "forest_concession",
            "transnational",
            "fully_updated",
            # base version mixin
            "created_at",
            "created_by",
            "modified_at",
            "modified_by",
            "sent_to_review_at",
            "sent_to_review_by",
            "sent_to_activation_at",
            "sent_to_activation_by",
            "activated_at",
            "activated_by",
            "status",
        )
        fields = "__all__"
        extra_kwargs = {
            "ds_quotations": {"required": True},
        }

    # @staticmethod
    # def get_operating_company(obj: DealVersion):
    #     if obj.operating_company and obj.operating_company.active_version:
    #         return {
    #             "id": obj.operating_company.id,
    #             "name": obj.operating_company.active_version.name,
    #         }
    #     return None

    @staticmethod
    def save_submodels(data, dv1: DealVersion):
        # TODO Later right now we're handling contracts, locations and datasources here
        #  in the serializer. not very pretty. maybe drf-writable-nested
        #  would be an alternative
        #  see: https://www.django-rest-framework.org/api-guide/relations/#writable-nested-serializers
        #  and: https://stackoverflow.com/questions/62847000/write-an-explicit-update-method-for-serializer

        l_nids = set()
        for location in data.get("locations"):
            l_nids.add(location["nid"])
            upserted_location, created = Location.objects.update_or_create(
                nid=location["nid"],
                dealversion=dv1,
                defaults={
                    "name": location["name"],
                    "description": location["description"],
                    "point": (
                        GEOSGeometry(str(location["point"]))
                        if location["point"]
                        else None
                    ),
                    "facility_name": location["facility_name"],
                    "level_of_accuracy": location["level_of_accuracy"],
                    "comment": location["comment"],
                },
            )

            areas = location.get("areas")
            if created:
                Area.objects.bulk_create(
                    [
                        Area(
                            location=upserted_location,
                            nid=area["nid"],
                            type=area["type"],
                            current=area["current"],
                            date=area["date"],
                            area=Area.geometry_to_multipolygon(area["area"]),
                        )
                        for area in areas
                    ]
                )
            else:
                a_nids = set()
                for area in areas:
                    upserted_area, _ = Area.objects.update_or_create(
                        nid=area["nid"],
                        location=upserted_location,
                        defaults={
                            "type": area["type"],
                            "current": area["current"],
                            "date": area["date"],
                            "area": Area.geometry_to_multipolygon(area["area"]),
                        },
                    )
                    a_nids.add(upserted_area.nid)

                Area.objects.filter(location=upserted_location).exclude(
                    nid__in=a_nids
                ).delete()

        Location.objects.filter(dealversion=dv1).exclude(nid__in=l_nids).delete()

        c_nids = set()
        for contract in data.get("contracts"):
            c_nids.add(contract["nid"])
            Contract.objects.update_or_create(
                nid=contract["nid"],
                dealversion=dv1,
                defaults={
                    "number": contract["number"],
                    "date": contract["date"],
                    "expiration_date": contract["expiration_date"],
                    "agreement_duration": contract["agreement_duration"],
                    "comment": contract["comment"],
                },
            )
        Contract.objects.filter(dealversion=dv1).exclude(nid__in=c_nids).delete()

        ds_nids = set()
        for datasource in data.get("datasources"):
            ds_nids.add(datasource["nid"])
            DealDataSource.objects.update_or_create(
                nid=datasource["nid"],
                dealversion=dv1,
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
        DealDataSource.objects.filter(dealversion=dv1).exclude(nid__in=ds_nids).delete()


BASE_WORKFLOW_INFO_FIELDS = (
    "id",
    "from_user_id",
    "to_user_id",
    "status_before",
    "status_after",
    "timestamp",
    "comment",
    "resolved",
    "replies",
)


class InvolvementSerializer(ReadOnlyModelSerializer):
    percentage = serializers.DecimalField(
        decimal_places=2,
        max_digits=5,
        coerce_to_string=True,
        allow_null=True,
    )

    class Meta:
        model = Involvement
        fields = [
            "id",
            "nid",
            "parent_investor_id",
            "child_investor_id",
            "role",
            "investment_type",
            "percentage",
            "loans_amount",
            "loans_currency_id",
            "loans_date",
            "parent_relation",
            "comment",
        ]


class DealWorkflowInfoSerializer(ReadOnlyModelSerializer):
    class Meta:
        model = DealWorkflowInfo
        fields = BASE_WORKFLOW_INFO_FIELDS + (
            "deal_id",
            "deal_version_id",
        )


class InvestorWorkflowInfoSerializer(ReadOnlyModelSerializer):
    class Meta:
        model = InvestorWorkflowInfo
        fields = BASE_WORKFLOW_INFO_FIELDS + (
            "investor_id",
            "investor_version_id",
        )


class DealSerializer(serializers.ModelSerializer[DealHull]):
    active_version_id = serializers.PrimaryKeyRelatedField[DealVersion](read_only=True)
    draft_version_id = serializers.PrimaryKeyRelatedField[DealVersion](read_only=True)
    first_created_by_id = serializers.PrimaryKeyRelatedField[User](read_only=True)

    country_id = serializers.PrimaryKeyRelatedField[Country](read_only=True)
    versions = serializers.SerializerMethodField()
    selected_version = DealVersionSerializer(read_only=True)

    workflowinfos = serializers.SerializerMethodField()

    class Meta:
        model = DealHull
        fields = "__all__"

    @extend_schema_field(DealVersionVersionsListSerializer(many=True, read_only=True))
    def get_versions(self, obj):
        user = self.context["request"].user

        if not is_reporter_or_higher(user):  # is anonymous
            q = Q(status=VersionStatus.ACTIVATED, is_public=True)
        elif not is_editor_or_higher(user):  # is reporter
            q = Q(status=VersionStatus.ACTIVATED, is_public=True) | Q(created_by=user)
        else:
            q = Q()

        qs_versions = obj.versions.filter(q)
        return DealVersionVersionsListSerializer(qs_versions, many=True).data

    @extend_schema_field(DealWorkflowInfoSerializer(many=True, read_only=True))
    def get_workflowinfos(self, obj):
        user = self.context["request"].user

        if not is_reporter_or_higher(user):  # is anonymous
            return []

        qs_wfis = obj.workflowinfos.all()
        return DealWorkflowInfoSerializer(qs_wfis, many=True).data


class InvestorVersionVersionsListSerializer(ReadOnlyModelSerializer):
    class Meta:
        model = InvestorVersion
        fields = [
            "id",
            "created_at",
            "created_by_id",
            "modified_at",
            "modified_by_id",
            "sent_to_review_at",
            "sent_to_review_by_id",
            "sent_to_activation_at",
            "sent_to_activation_by_id",
            "activated_at",
            "activated_by_id",
            "status",
        ]


class InvestorDataSourceSerializer(_BaseDataSourceSerializer):
    class Meta:
        model = InvestorDataSource
        fields = "__all__"


class Investor2DealSerializer(serializers.ModelSerializer):
    class Meta:
        model = DealVersion
        fields = ["id", "deal_id"]


class InvestorVersionSerializer(MyModelSerializer):
    country_id = serializers.PrimaryKeyRelatedField[Country](read_only=True)

    # creating these because DRF shows these fields as "created_by", instead of "~_id"
    created_by_id = serializers.PrimaryKeyRelatedField[User](read_only=True)
    modified_by_id = serializers.PrimaryKeyRelatedField[User](read_only=True)
    sent_to_review_by_id = serializers.PrimaryKeyRelatedField[User](read_only=True)
    sent_to_activation_by_id = serializers.PrimaryKeyRelatedField[User](read_only=True)
    activated_by_id = serializers.PrimaryKeyRelatedField[User](read_only=True)

    # not truly read-only since they get written manually
    involvements = serializers.SerializerMethodField(read_only=True)
    datasources = InvestorDataSourceSerializer(many=True, read_only=True)

    class Meta:
        model = InvestorVersion
        read_only_fields = (
            "id",
            "investor",
            # calculated fields
            "name_unknown",
            # base version mixin
            "created_at",
            "created_by",
            "modified_at",
            "modified_by",
            "sent_to_review_at",
            "sent_to_review_by",
            "sent_to_activation_at",
            "sent_to_activation_by",
            "activated_at",
            "activated_by",
            "status",
        )
        exclude = ("involvements_snapshot",)
        extra_kwargs = {
            "ds_quotations": {"required": True},
        }

    @staticmethod
    @extend_schema_field(InvolvementSerializer(many=True, read_only=True))
    def get_involvements(obj) -> list[Involvement]:
        return obj.involvements_snapshot

    @staticmethod
    def save_submodels(data, iv1: InvestorVersion):
        iv1.involvements_snapshot = data["involvements"]

        # TODO Later right now we're handling datasources here
        #  in the serializer. not very pretty. maybe drf-writable-nested
        #  would be an alternative
        #  see: https://www.django-rest-framework.org/api-guide/relations/#writable-nested-serializers
        #  and: https://stackoverflow.com/questions/62847000/write-an-explicit-update-method-for-serializer

        ds_nids = set()
        for datasource in data.get("datasources"):
            ds_nids.add(datasource["nid"])
            InvestorDataSource.objects.update_or_create(
                nid=datasource["nid"],
                investorversion=iv1,
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
        InvestorDataSource.objects.filter(investorversion=iv1).exclude(
            nid__in=ds_nids
        ).delete()


# Not actively used, just for drf_spectacular types (and tests)
class SimpleInvestorSerializer(serializers.Serializer):
    id = serializers.IntegerField()

    name = serializers.CharField(allow_null=True)
    name_unknown = serializers.BooleanField(allow_null=True)
    country_id = serializers.IntegerField(allow_null=True)
    classification = serializers.CharField(allow_null=True)

    active = serializers.BooleanField()
    deleted = serializers.BooleanField()


class InvestorDealSelectedVersionSerializer(ReadOnlyModelSerializer):
    class Meta:
        model = DealVersion
        fields = (
            "id",
            "current_intention_of_investment",
            "current_negotiation_status",
            "current_implementation_status",
            "deal_size",
        )


class InvestorDealSerializer(ReadOnlyModelSerializer):
    selected_version = serializers.SerializerMethodField(read_only=True)

    @extend_schema_field(InvestorDealSelectedVersionSerializer)
    def get_selected_version(self, obj: DealHull):
        return InvestorDealSelectedVersionSerializer(obj.active_version).data

    class Meta:
        model = DealHull
        fields = ("id", "country_id", "selected_version")


class InvestorSerializer(serializers.ModelSerializer[InvestorHull]):
    active_version_id = serializers.PrimaryKeyRelatedField[InvestorVersion](
        read_only=True
    )
    draft_version_id = serializers.PrimaryKeyRelatedField[InvestorVersion](
        read_only=True
    )
    first_created_by_id = serializers.PrimaryKeyRelatedField[User](read_only=True)

    versions = serializers.SerializerMethodField(read_only=True)

    selected_version = InvestorVersionSerializer()
    deals = serializers.SerializerMethodField(read_only=True)

    parents = serializers.SerializerMethodField(read_only=True)
    children = serializers.SerializerMethodField(read_only=True)

    workflowinfos = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = InvestorHull
        fields = "__all__"

    @extend_schema_field(
        InvestorVersionVersionsListSerializer(many=True, read_only=True)
    )
    def get_versions(self, obj):
        user: User = self.context["request"].user

        if not is_reporter_or_higher(user):  # is anonymous
            q = Q(status=VersionStatus.ACTIVATED)
        elif not is_editor_or_higher(user):  # is reporter
            q = Q(status=VersionStatus.ACTIVATED) | Q(created_by=user)
        else:
            q = Q()

        qs_versions = obj.versions.filter(q)
        return InvestorVersionVersionsListSerializer(qs_versions, many=True).data

    @extend_schema_field(InvestorWorkflowInfoSerializer(many=True, read_only=True))
    def get_workflowinfos(self, obj):
        user = self.context["request"].user

        if not is_reporter_or_higher(user):  # is anonymous
            return []

        qs_wfis = obj.workflowinfos.all()
        return InvestorWorkflowInfoSerializer(qs_wfis, many=True).data

    @extend_schema_field(InvestorDealSerializer(many=True))
    def get_deals(self, obj: InvestorHull):
        user: User = self.context["request"].user

        version_ids = obj.dealversions.values_list("id", flat=True).distinct()

        qs = DealHull.objects.filter(active_version_id__in=version_ids)
        qs = qs.public() if not is_reporter_or_higher(user) else qs

        return InvestorDealSerializer(qs, many=True).data

    @extend_schema_field(InvolvementSerializer(many=True))
    def get_children(self, obj: InvestorHull):
        user: User = self.context["request"].user

        qs = obj.get_children()
        qs = qs.active() if not is_reporter_or_higher(user) else qs

        return InvolvementSerializer(qs, read_only=True, many=True).data

    @extend_schema_field(InvolvementSerializer(many=True))
    def get_parents(self, obj: InvestorHull):
        user: User = self.context["request"].user

        if hasattr(obj, "_selected_version_id"):
            version = obj.versions.get(id=obj._selected_version_id)
        else:
            version = obj.active_version or obj.draft_version

        # just take snapshot here, because it is set correctly for activated versions
        snapshot = version.involvements_snapshot or []

        if not is_reporter_or_higher(user):
            parent_ids = [inv["parent_investor_id"] for inv in snapshot]
            active_parent_ids = (
                InvestorHull.objects.filter(id__in=parent_ids)
                .active()
                .values_list("id", flat=True)
            )
            return [
                inv
                for inv in snapshot
                if inv["parent_investor_id"] in active_parent_ids
            ]

        return snapshot


class ContextHelpSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)

    class Meta:
        model = ContextHelp
        fields = "__all__"
