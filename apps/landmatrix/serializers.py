from django.contrib.gis.geos import GEOSGeometry
from django.db.models import Q, QuerySet, F
from django.db.models.functions import JSONObject
from django.utils.translation import gettext as _
from rest_framework import serializers

from apps.landmatrix.models import FieldDefinition
from apps.landmatrix.models.country import Country, Region
from apps.landmatrix.models.currency import Currency
from apps.landmatrix.models.new import (
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


class FieldDefinitionSerializer(serializers.ModelSerializer):
    class Meta:
        model = FieldDefinition
        fields = "__all__"


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

        # deals { id }


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


# ########## NEW MODEL
# class UserIdUsernameSerialiser(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = ["id", "username"]


class DealVersionVersionsListSerializer(serializers.ModelSerializer):
    class Meta:
        model = DealVersion2
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


class DealVersionSerializer(serializers.ModelSerializer):
    locations = LocationSerializer(many=True, read_only=True)
    contracts = ContractSerializer(many=True, read_only=True)
    datasources = DealDataSourceSerializer(many=True, read_only=True)
    # operating_company = serializers.SerializerMethodField()
    operating_company_id = serializers.PrimaryKeyRelatedField(read_only=True)

    # creating these because DRF shows these fields as "created_by", instead of "~_id"
    created_by_id = serializers.PrimaryKeyRelatedField(read_only=True)
    modified_by_id = serializers.PrimaryKeyRelatedField(read_only=True)
    sent_to_review_by_id = serializers.PrimaryKeyRelatedField(read_only=True)
    sent_to_activation_by_id = serializers.PrimaryKeyRelatedField(read_only=True)
    activated_by_id = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = DealVersion2
        read_only_fields = (
            "id",
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

    # @staticmethod
    # def get_operating_company(obj: DealVersion2):
    #     if obj.operating_company and obj.operating_company.active_version:
    #         return {
    #             "id": obj.operating_company.id,
    #             "name": obj.operating_company.active_version.name,
    #         }
    #     return None

    @staticmethod
    def save_submodels(data, dv1: DealVersion2):
        # FIXME right now we're handling contracts, locations and datasources here
        #  in the serializer. not very pretty. maybe drf-writable-nested
        #  would be an alternative

        l_nids = set()
        for location in data.get("locations"):
            l_nids.add(location["nid"])
            upserted_location, created = Location.objects.update_or_create(
                nid=location["nid"],
                dealversion=dv1,
                defaults={
                    "name": location["name"],
                    "description": location["description"],
                    "point": GEOSGeometry(str(location["point"]))
                    if location["point"]
                    else None,
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
                            type=area["type"],
                            current=area["current"],
                            date=area["date"],
                            area=GEOSGeometry(str(area["area"])),
                        )
                        for area in areas
                    ]
                )
            else:
                a_ids = set()
                for area in areas:
                    upserted_area, _ = Area.objects.update_or_create(
                        id=area["id"],
                        location=upserted_location,
                        defaults={
                            "type": area["type"],
                            "current": area["current"],
                            "date": area["date"],
                            "area": GEOSGeometry(str(area["area"])),
                        },
                    )
                    a_ids.add(upserted_area.id)

                Area.objects.filter(location=upserted_location).exclude(
                    id__in=a_ids
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


class DealSerializer(serializers.ModelSerializer):
    active_version_id = serializers.PrimaryKeyRelatedField(read_only=True)
    draft_version_id = serializers.PrimaryKeyRelatedField(read_only=True)
    created_by_id = serializers.PrimaryKeyRelatedField(read_only=True)

    country_id = serializers.PrimaryKeyRelatedField(read_only=True)
    versions = DealVersionVersionsListSerializer(many=True, read_only=True)
    selected_version = DealVersionSerializer(read_only=True)
    workflowinfos = serializers.SerializerMethodField(read_only=True)

    @staticmethod
    def get_workflowinfos(obj: DealHull):
        wfis: QuerySet[DealWorkflowInfo2] = DealWorkflowInfo2.objects.filter(
            deal_id=obj.id
        )
        return [dwi.to_dict() for dwi in wfis.order_by("-timestamp")]

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
    country_id = serializers.PrimaryKeyRelatedField(read_only=True)

    # creating these because DRF shows these fields as "created_by", instead of "~_id"
    created_by_id = serializers.PrimaryKeyRelatedField(read_only=True)
    modified_by_id = serializers.PrimaryKeyRelatedField(read_only=True)
    sent_to_review_by_id = serializers.PrimaryKeyRelatedField(read_only=True)
    sent_to_activation_by_id = serializers.PrimaryKeyRelatedField(read_only=True)
    activated_by_id = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = InvestorVersion2
        read_only_fields = (
            "id",
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

    @staticmethod
    def save_submodels(data, iv1: InvestorVersion2):
        # FIXME right now we're handling datasources here
        #  in the serializer. not very pretty. maybe drf-writable-nested
        #  would be an alternative
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


class InvestorSerializer(serializers.ModelSerializer):
    active_version_id = serializers.PrimaryKeyRelatedField(read_only=True)
    draft_version_id = serializers.PrimaryKeyRelatedField(read_only=True)

    versions = InvestorVersionVersionsListSerializer(many=True)

    selected_version = InvestorVersionSerializer()
    deals = serializers.SerializerMethodField()

    # involvements = InvolvementSerializer(many=True)
    involvements = serializers.SerializerMethodField()
    workflowinfos = serializers.SerializerMethodField()

    class Meta:
        model = InvestorHull
        fields = "__all__"

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
                "country_id": d.country_id,
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

    def get_involvements(self, obj: InvestorHull):
        if hasattr(obj, "_selected_version_id"):
            selected_version_id = obj._selected_version_id
        else:
            selected_version_id = None

        if selected_version_id and selected_version_id != obj.active_version_id:
            invos = obj.versions.get(id=selected_version_id).involvements_snapshot
        elif obj.active_version:
            invos = (
                Involvement.objects.filter(
                    Q(parent_investor_id=obj.id) | Q(child_investor_id=obj.id)
                )
                .filter(
                    ~Q(parent_investor__active_version=None),
                    ~Q(child_investor__active_version=None),
                )
                .values(
                    "id",
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
                )
            )

        else:
            # TODO should the draft version also have this involvements_snapshot?
            invos = obj.draft_version.involvements_snapshot
        self._enrich_involvements_for_viewing(invos, obj.id)
        return invos

    @staticmethod
    def _enrich_involvements_for_viewing(
        involvements: list[dict], target_id: int
    ) -> None:
        all_ids = set()
        for involvement in involvements:
            all_ids.add(involvement["parent_investor_id"])
            all_ids.add(involvement["child_investor_id"])
        investors = {
            x["id"]: x
            for x in InvestorHull.objects.filter(id__in=all_ids)
            .annotate(
                selected_version=JSONObject(
                    name=F("active_version__name"),
                    name_unknown=F("active_version__name_unknown"),
                    country_id=F("active_version__country_id"),
                    classification=F("active_version__classification"),
                )
            )
            .values("id", "selected_version", "deleted")
        }

        for invo in involvements:
            if target_id == invo["parent_investor_id"]:
                relationship = (
                    _("Subsidiary company")
                    if invo["role"] == "PARENT"
                    else _("Beneficiary company")
                )
                other_investor = investors[invo["child_investor_id"]]
            elif target_id == invo["child_investor_id"]:
                relationship = (
                    _("Parent company")
                    if invo["role"] == "PARENT"
                    else _("Tertiary investor/lender")
                )
                other_investor = investors[invo["parent_investor_id"]]
            else:
                continue

            invo |= {"relationship": relationship, "other_investor": other_investor}

    # def get_deals(self):
    #     return

    @staticmethod
    def get_workflowinfos(obj: InvestorHull):
        wfis: QuerySet[InvestorWorkflowInfo2] = InvestorWorkflowInfo2.objects.filter(
            investor_id=obj.id
        )
        return [x.to_dict() for x in wfis.order_by("-id")]
