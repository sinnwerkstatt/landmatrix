from rest_framework import serializers


class ChartDescriptions(serializers.Serializer):
    web_of_transnational_deals = serializers.CharField()
    dynamics_overview = serializers.CharField()
    produce_info_map = serializers.CharField()
    global_web_of_investments = serializers.CharField()
