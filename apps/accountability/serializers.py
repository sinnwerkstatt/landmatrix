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
    country_id = serializers.ReadOnlyField(source="deal.country_id")
    class Meta:
        model = DealScore
        fields = ["deal", "test", "country_id"]

class DealVariableSerializer(serializers.ModelSerializer):
    class Meta:
        model = DealVariable
        fields = ["id", "deal_score", "vggt_variable", "status", "score"]