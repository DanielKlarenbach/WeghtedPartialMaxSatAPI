from rest_framework import serializers


class ClauseSerializer(serializers.Serializer):
    variables = serializers.ListField(
        child=serializers.IntegerField()
    )
    weight = serializers.IntegerField(min_value=0)
