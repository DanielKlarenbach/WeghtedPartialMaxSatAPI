from rest_framework import serializers


class ClauseSerializer(serializers.Serializer):
    variables = serializers.IntegerField(
        many=True,
        allow_empty=False
    )
    weight = serializers.IntegerField(min_value=0)


class ClauseListSerializer(serializers.Serializer):
    clauses = ClauseSerializer(many=True, allow_empty=False)
