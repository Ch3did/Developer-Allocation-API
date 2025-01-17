from rest_framework import serializers

from ..models import Project
from .technology import TechnologySerializer


class ProjectSerializer(serializers.ModelSerializer):
    technologies = TechnologySerializer(many=True)

    class Meta:
        model = Project
        fields = "__all__"


class ProjectSerializerUpdate(serializers.Serializer):
    project_id = serializers.IntegerField(write_only=True, required=True)
    technologies_id = serializers.ListField(
        child=serializers.IntegerField(), write_only=True, required=True
    )
    name = serializers.CharField(write_only=True, required=False)
    data_inicial = serializers.DateField(required=False, allow_null=True)
    data_final = serializers.DateField(required=False, allow_null=True)
    hours_por_dia = serializers.IntegerField(required=False, default=8)


class ProjectSerializerCreate(serializers.Serializer):
    technologies_id = serializers.ListField(
        child=serializers.IntegerField(), write_only=True, required=True
    )
    name = serializers.CharField(write_only=True, required=False)
    data_inicial = serializers.DateField(required=False, allow_null=True)
    data_final = serializers.DateField(required=False, allow_null=True)
    hours_por_dia = serializers.IntegerField(required=False, default=8)
