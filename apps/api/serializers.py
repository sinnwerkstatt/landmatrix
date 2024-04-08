from rest_framework import serializers


class SearchedInvestorSerializer(serializers.Serializer):
    class SelectedInvestorVersionSerializer(serializers.Serializer):
        id = serializers.IntegerField()
        name = serializers.CharField()
        country_id = serializers.IntegerField()
        modified_at = serializers.DateTimeField()
        country_name = serializers.CharField()
        name_unknown = serializers.BooleanField()

    id = serializers.IntegerField()
    active_version_id = serializers.IntegerField()
    draft_version_id = serializers.IntegerField()
    deleted = serializers.BooleanField()
    first_created_at = serializers.DateTimeField()
    first_created_by_id = serializers.IntegerField()
    selected_version = SelectedInvestorVersionSerializer()


class ChartDescriptions(serializers.Serializer):
    web_of_transnational_deals = serializers.CharField()
    dynamics_overview = serializers.CharField()
    produce_info_map = serializers.CharField()
    global_web_of_investments = serializers.CharField()
