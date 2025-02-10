from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers

from apps.accountability.models import (
    Bookmark,
    DealScore,
    DealScoreVersion,
    DealVariable,
    Filters,
    Project,
    UserInfo,
    VggtArticle,
    VggtChapter,
    VggtVariable,
)
from apps.landmatrix.models.country import Country
from apps.landmatrix.serializers import CountrySerializer


class UserInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserInfo
        fields = "__all__"
        read_only_fields = ["user"]


class VggtChapterSerializer(serializers.ModelSerializer):
    class Meta:
        model = VggtChapter
        fields = "__all__"


class VggtArticleSerializer(serializers.ModelSerializer):
    title = serializers.ReadOnlyField(source="chapter.name")

    class Meta:
        model = VggtArticle
        fields = "__all__"


class VggtVariableSerializer(serializers.ModelSerializer):
    class Meta:
        model = VggtVariable
        fields = "__all__"

    def create(self, validated_data):
        articles_data = validated_data.pop("articles")
        variable = VggtVariable.objects.create(**validated_data)
        variable.articles.set(articles_data)
        score_versions = DealScoreVersion.objects.all()
        for score in score_versions:
            DealVariable.objects.create(deal_score=score, vggt_variable=variable)
        return variable


class DealVariableSerializer(serializers.ModelSerializer):
    class Meta:
        model = DealVariable
        fields = [
            "vggt_variable",
            "status",
            "score",
            "scored_at",
            "scored_by",
            "assignee",
        ]


class DealScoreVersionSerializer(serializers.ModelSerializer):
    variables = DealVariableSerializer(many=True)

    class Meta:
        model = DealScoreVersion
        fields = ["deal_version", "status", "variables"]


class DealScoreSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField(source="deal.id")
    score = DealScoreVersionSerializer(source="current_score")

    """
    Filters and general information
    """
    region_id = serializers.ReadOnlyField(source="deal.country.region_id")
    country = (
        serializers.SerializerMethodField()
    )  # Empty field to include country as .annotate() in views.py
    deal_size = serializers.ReadOnlyField(source="deal.active_version.deal_size")
    negotiation_status = serializers.ReadOnlyField(
        source="deal.active_version.current_negotiation_status"
    )
    nature_of_deal = serializers.ReadOnlyField(
        source="deal.active_version.nature_of_deal"
    )
    operating_company = (
        serializers.SerializerMethodField()
    )  # Empty field to include operating_company as .annotate() in views.py
    # NOTE: Currently not in use -> Fix later
    # involved_actors = ActorsSchemaField(source="deal.active_version.involved_actors")
    initiation_year = serializers.ReadOnlyField(
        source="deal.active_version.initiation_year"
    )
    implementation_status = serializers.ReadOnlyField(
        source="deal.active_version.current_implementation_status"
    )
    intention_of_investment = serializers.ReadOnlyField(
        source="deal.active_version.current_intention_of_investment"
    )
    crops = serializers.ReadOnlyField(source="deal.active_version.current_crops")
    animals = serializers.ReadOnlyField(source="deal.active_version.current_animals")
    minerals = serializers.ReadOnlyField(source="deal.active_version.current_minerals")
    transnational = serializers.ReadOnlyField(
        source="deal.active_version.transnational"
    )
    forest_concession = serializers.ReadOnlyField(
        source="deal.active_version.forest_concession"
    )
    # is_public = serializers.ReadOnlyField(source="deal.active_version.is_public")

    """
    Additional VGGTs scoring fields
    """
    recognition_status = serializers.ReadOnlyField(
        source="deal.active_version.recognition_status"
    )
    recognition_status_comment = serializers.ReadOnlyField(
        source="deal.active_version.recognition_status_comment"
    )
    displacement_of_people = serializers.ReadOnlyField(
        source="deal.active_version.displacement_of_people"
    )
    displaced_people = serializers.ReadOnlyField(
        source="deal.active_version.displaced_people"
    )
    displaced_households = serializers.ReadOnlyField(
        source="deal.active_version.displaced_households"
    )
    displaced_people_from_community_land = serializers.ReadOnlyField(
        source="deal.active_version.displaced_people_from_community_land"
    )
    displaced_people_within_community_land = serializers.ReadOnlyField(
        source="deal.active_version.displaced_people_within_community_land"
    )
    displaced_households_from_fields = serializers.ReadOnlyField(
        source="deal.active_version.displaced_households_from_fields"
    )
    displaced_people_on_completion = serializers.ReadOnlyField(
        source="deal.active_version.displaced_people_on_completion"
    )
    displacement_of_people_comment = serializers.ReadOnlyField(
        source="deal.active_version.displacement_of_people_comment"
    )
    promised_compensation = serializers.ReadOnlyField(
        source="deal.active_version.promised_compensation"
    )
    received_compensation = serializers.ReadOnlyField(
        source="deal.active_version.received_compensation"
    )
    community_consultation = serializers.ReadOnlyField(
        source="deal.active_version.community_consultation"
    )
    community_consultation_comment = serializers.ReadOnlyField(
        source="deal.active_version.community_consultation_comment"
    )
    land_conflicts = serializers.ReadOnlyField(
        source="deal.active_version.land_conflicts"
    )
    land_conflicts_comment = serializers.ReadOnlyField(
        source="deal.active_version.land_conflicts_comment"
    )
    negative_impacts = serializers.ReadOnlyField(
        source="deal.active_version.negative_impacts"
    )
    negative_impacts_comment = serializers.ReadOnlyField(
        source="deal.active_version.negative_impacts_comment"
    )
    materialized_benefits = serializers.ReadOnlyField(
        source="deal.active_version.materialized_benefits"
    )
    materialized_benefits_comment = serializers.ReadOnlyField(
        source="deal.active_version.materialized_benefits_comment"
    )
    contract_farming = serializers.ReadOnlyField(
        source="deal.active_version.contract_farming"
    )
    contract_farming_comment = serializers.ReadOnlyField(
        source="deal.active_version.contract_farming_comment"
    )
    promised_benefits = serializers.ReadOnlyField(
        source="deal.active_version.promised_benefits"
    )
    promised_benefits_comment = serializers.ReadOnlyField(
        source="deal.active_version.promised_benefits_comment"
    )
    water_extraction_envisaged = serializers.ReadOnlyField(
        source="deal.active_version.water_extraction_envisaged"
    )
    water_extraction_envisaged_comment = serializers.ReadOnlyField(
        source="deal.active_version.water_extraction_envisaged_comment"
    )
    source_of_water_extraction = serializers.ReadOnlyField(
        source="deal.active_version.source_of_water_extraction"
    )
    source_of_water_extraction_comment = serializers.ReadOnlyField(
        source="deal.active_version.source_of_water_extraction_comment"
    )
    community_reaction = serializers.ReadOnlyField(
        source="deal.active_version.community_reaction"
    )
    community_reaction_comment = serializers.ReadOnlyField(
        source="deal.active_version.community_reaction_comment"
    )
    gender_related_information = serializers.ReadOnlyField(
        source="deal.active_version.gender_related_information"
    )
    purchase_price = serializers.ReadOnlyField(
        source="deal.active_version.purchase_price"
    )
    purchase_price_area = serializers.ReadOnlyField(
        source="deal.active_version.purchase_price_area"
    )
    # purchase_price_currency = serializers.ReadOnlyField(source="deal.active_version.purchase_price_currency")
    purchase_price_comment = serializers.ReadOnlyField(
        source="deal.active_version.purchase_price_comment"
    )
    annual_leasing_fee = serializers.ReadOnlyField(
        source="deal.active_version.annual_leasing_fee"
    )
    annual_leasing_fee_area = serializers.ReadOnlyField(
        source="deal.active_version.annual_leasing_fee_area"
    )
    # annual_leasing_fee_currency = serializers.ReadOnlyField(source="deal.active_version.annual_leasing_fee_currency")
    annual_leasing_fee_comment = serializers.ReadOnlyField(
        source="deal.active_version.annual_leasing_fee_comment"
    )
    presence_of_organizations = serializers.ReadOnlyField(
        source="deal.active_version.presence_of_organizations"
    )

    class Meta:
        model = DealScore
        exclude = ["deal"]

    def get_country(self, obj):  # Get .annotate() field "country" from views.py
        try:
            return obj.country
        except:
            return None

    def get_operating_company(
        self, obj
    ):  # Get .annotate() field "operating_company" from views.py
        try:
            return obj.operating_company
        except:
            return None


# class DealVariableSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = DealVariable
#         fields = "__all__"


# class DealVariableSerializerSimple(serializers.ModelSerializer):
#     class Meta:
#         model = DealVariable
#         fields = ["vggt_variable", "status", "score"]

# class DealScoreSerializer(serializers.ModelSerializer):
#     region_id = serializers.ReadOnlyField(source="deal.country.region_id")
#     country_id = serializers.ReadOnlyField(source="deal.country_id")
#     deal_size = serializers.ReadOnlyField(source="deal.active_version.deal_size")
#     negotiation_status = serializers.ReadOnlyField(source="deal.active_version.current_negotiation_status")
#     nature_of_deal = serializers.ReadOnlyField(source="deal.active_version.nature_of_deal")
#     operating_company = serializers.ReadOnlyField(source="deal.active_version.operating_company_id")
#     involved_actors = serializers.ReadOnlyField(source="deal.active_version.involved_actors")
#     initiation_year = serializers.ReadOnlyField(source="deal.active_version.initiation_year")
#     implementation_status = serializers.ReadOnlyField(source="deal.active_version.current_implementation_status")
#     intention_of_investment = serializers.ReadOnlyField(source="deal.active_version.current_intention_of_investment")
#     crops = serializers.ReadOnlyField(source="deal.active_version.current_crops")
#     animals = serializers.ReadOnlyField(source="deal.active_version.current_animals")
#     minerals = serializers.ReadOnlyField(source="deal.active_version.current_minerals")
#     transnational = serializers.ReadOnlyField(source="deal.active_version.transnational")
#     forest_concession = serializers.ReadOnlyField(source="deal.active_version.forest_concession")
#     is_public = serializers.ReadOnlyField(source="deal.active_version.is_public")
#     score = DealVariableSerializerSimple(read_only=True, many=True)
#     class Meta:
#         model = DealScore
#         fields = [
#             "deal",
#             "test",
#             "region_id",
#             "country_id",
#             "deal_size",
#             "negotiation_status",
#             "nature_of_deal",
#             "operating_company",
#             "involved_actors",
#             "initiation_year",
#             "implementation_status",
#             "intention_of_investment",
#             "crops", "animals", "minerals",
#             "transnational",
#             "forest_concession",
#             "is_public",
#             "score",
#         ]


class FiltersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Filters
        fields = "__all__"
        read_only_fields = ["project"]


class ProjectSerializer(serializers.ModelSerializer):
    filters = FiltersSerializer()

    class Meta:
        model = Project
        fields = "__all__"
        read_only_fields = ["owner", "created_at", "modified_at", "modified_by"]

    def create(self, validated_data):
        filters_data = validated_data.pop("filters")
        editors_data = validated_data.pop("editors")
        project = Project.objects.create(**validated_data)
        project.editors.set(editors_data)
        Filters.objects.create(project=project, **filters_data)
        return project

    def update(self, instance, validated_data):
        filters_data = validated_data.pop("filters")
        editors_data = validated_data.pop("editors")
        for field, value in filters_data.items():
            setattr(instance.filters, field, value)
            instance.filters.save()
        if name := validated_data.get("name"):
            instance.name = name
        if description := validated_data.get("description"):
            instance.description = description
        instance.editors.set(editors_data)
        instance.save()
        return instance


class BookmarkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bookmark
        fields = ["id", "order", "project"]
        read_only_fields = ["user"]


class BookmarkBulkSerializer(serializers.ModelSerializer):
    bookmarks = BookmarkSerializer(many=True)

    class Meta:
        model = Bookmark
        fields = "__all__"
        # depth = 1
