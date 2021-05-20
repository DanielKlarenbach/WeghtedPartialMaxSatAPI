from rest_framework import serializers

from api.models import Clause


class ClauseSerializer(serializers.Serializer):
    variables = serializers.ListSerializer(
        child=serializers.IntegerField(),
        allow_empty=False
    )
    weight = serializers.IntegerField(min_value=0)

    def create(self, validated_data):
        return Clause(**validated_data)


class ClauseListSerializer(serializers.Serializer):
    clauses = ClauseSerializer(many=True, allow_empty=False)

    def create(self, validated_data):
        clauses = []
        for data in validated_data['clauses']:
            serializer = ClauseSerializer(data=data)
            serializer.is_valid(raise_exception=True)
            clause = serializer.save()
            clauses.append(clause)
        return clauses
