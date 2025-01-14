from rest_framework import serializers

from ..models import Programador
from .tecnologia_serializer import TecnologiaSerializer


class ProgramadorSerializer(serializers.ModelSerializer):
    tecnologias = TecnologiaSerializer(many=True)

    class Meta:
        model = Programador
        fields = "__all__"


class ProgramadorSerializerUpdate(serializers.Serializer):
    programador_id = serializers.IntegerField(write_only=True, required=True)
    tecnologias_id = serializers.ListField(
        child=serializers.IntegerField(), write_only=True, required=True
    )
    nome = serializers.CharField(write_only=True, required=False)


class ProgramadorSerializerCreate(serializers.Serializer):
    tecnologias_id = serializers.ListField(
        child=serializers.IntegerField(), write_only=True, required=True
    )
    nome = serializers.CharField(write_only=True, required=False)
