from rest_framework import serializers


# https://stackoverflow.com/a/52467796
# https://github.com/tfranzel/drf-spectacular/issues/810
class ReadOnlyModelSerializer(serializers.ModelSerializer):
    def get_fields(self, *args, **kwargs):
        fields = super().get_fields(*args, **kwargs)
        for field in fields:
            fields[field].read_only = True
        return fields
