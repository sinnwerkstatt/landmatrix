from rest_framework import serializers

from drf_spectacular.utils import extend_schema_field

from apps.accountability.models import VggtChapter, VggtArticle, VggtVariable
from apps.accountability.models import DealScore, DealScoreVersion, DealVariable
from apps.accountability.models import Project, Filters
from apps.accountability.models import UserInfo, Bookmark

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
    class Meta:
        model = VggtArticle
        fields = "__all__"

class VggtVariableSerializer(serializers.ModelSerializer):
    class Meta:
        model = VggtVariable
        fields = "__all__"
    
    def create(self, validated_data):
        variable = VggtVariable.objects.create(**validated_data)
        score_versions = DealScoreVersion.objects.all()
        for score in score_versions:
            DealVariable.objects.create(deal_score=score, vggt_variable=variable)
        return variable

class DealVariableSerializer(serializers.ModelSerializer):
    class Meta:
        model = DealVariable
        fields = "__all__"


class DealScoreVersionSerializer(serializers.ModelSerializer):
    variables = DealVariableSerializer(many=True)
    class Meta:
        model = DealScoreVersion
        fields = "__all__"


class DealScoreSerializer(serializers.ModelSerializer):
    score = DealScoreVersionSerializer(source="current_score")
    class Meta:
        model = DealScore
        fields = "__all__"

        
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
        filters_data = validated_data.pop('filters')
        editors_data = validated_data.pop('editors')
        project = Project.objects.create(**validated_data)
        project.editors.set(editors_data)
        Filters.objects.create(project=project, **filters_data)
        return project

    def update(self, instance, validated_data):
        filters_data = validated_data.pop('filters')
        editors_data = validated_data.pop('editors')
        for field, value in filters_data.items():
            setattr(instance.filters, field, value)
            instance.filters.save()
        if name := validated_data.get('name'):
            instance.name = name
        if description := validated_data.get('description'):
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