from rest_framework import serializers

from ..models import Developers
from .technology import TechnologySerializer


class DevelopersSerializer(serializers.ModelSerializer):
    technologies = TechnologySerializer(many=True)

    class Meta:
        model = Developers
        fields = "__all__"


class DevelopersSerializerUpdate(serializers.Serializer):
    developer_id = serializers.IntegerField(write_only=True, required=True)
    technologies_id = serializers.ListField(
        child=serializers.IntegerField(), write_only=True, required=True
    )
    name = serializers.CharField(write_only=True, required=False)


class DevelopersSerializerCreate(serializers.Serializer):
    technologies_id = serializers.ListField(
        child=serializers.IntegerField(), write_only=True, required=True
    )
    name = serializers.CharField(write_only=True, required=False)
