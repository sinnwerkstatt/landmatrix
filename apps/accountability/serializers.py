from rest_framework import serializers
from apps.accountability.models import VggtChapter, VggtArticle, VggtVariable
from apps.accountability.models import DealScore, DealVariable

class VggtChapterSerializer(serializers.ModelSerializer):
    class Meta:
        model = VggtChapter
        fields = ["chapter", "name"]

class VggtArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = VggtArticle
        fields = ["id", "chapter", "article", "description"]

class VggtVariableSerializer(serializers.ModelSerializer):
    class Meta:
        model = VggtVariable
        fields = ["id", "number", "name", "landmatrix_fields", "landmatrix_additional_fields", "scoring_help"]

class DealScoreSerializer(serializers.ModelSerializer):
    region_id = serializers.ReadOnlyField(source="deal.country.region_id")
    country_id = serializers.ReadOnlyField(source="deal.country_id")
    deal_size = serializers.ReadOnlyField(source="deal.active_version.deal_size")
    negotiation_status = serializers.ReadOnlyField(source="deal.active_version.current_negotiation_status")
    nature_of_deal = serializers.ReadOnlyField(source="deal.active_version.nature_of_deal")
    operating_company = serializers.ReadOnlyField(source="deal.active_version.operating_company_id")
    involved_actors = serializers.ReadOnlyField(source="deal.active_version.involved_actors")
    # parent_companies = serializers.ReadOnlyField(source="deal.active_version.parent_companies")
    # top_investors = serializers.ReadOnlyField(source="deal.active_version.top_investors")
    initiation_year = serializers.ReadOnlyField(source="deal.active_version.initiation_year")
    implementation_status = serializers.ReadOnlyField(source="deal.active_version.current_implementation_status")
    intention_of_investment = serializers.ReadOnlyField(source="deal.active_version.current_intention_of_investment")
    crops = serializers.ReadOnlyField(source="deal.active_version.current_crops")
    animals = serializers.ReadOnlyField(source="deal.active_version.current_animals")
    minerals = serializers.ReadOnlyField(source="deal.active_version.current_minerals")
    transnational = serializers.ReadOnlyField(source="deal.active_version.transnational")
    forest_concession = serializers.ReadOnlyField(source="deal.active_version.forest_concession")
    is_public = serializers.ReadOnlyField(source="deal.active_version.is_public")

    class Meta:
        model = DealScore
        fields = [
            "deal",
            "test",
            "region_id",
            "country_id",
            "deal_size",
            "negotiation_status",
            "nature_of_deal",
            "operating_company",
            "involved_actors",
            # "parent_companies",
            # "top_investors",
            "initiation_year",
            "implementation_status",
            "intention_of_investment",
            "crops", "animals", "minerals",
            "transnational",
            "forest_concession",
            "is_public",
        ]

class DealVariableSerializer(serializers.ModelSerializer):
    class Meta:
        model = DealVariable
        fields = ["id", "deal_score", "vggt_variable", "status", "score"]