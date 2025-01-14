from rest_framework import serializers

from ..models import Projeto
from .tecnologia_serializer import TecnologiaSerializer


class ProjetoSerializer(serializers.ModelSerializer):
    tecnologias = TecnologiaSerializer(many=True)

    class Meta:
        model = Projeto
        fields = "__all__"


class ProjetoSerializerUpdate(serializers.Serializer):
    projeto_id = serializers.IntegerField(write_only=True, required=True)
    tecnologias_id = serializers.ListField(
        child=serializers.IntegerField(), write_only=True, required=True
    )
    nome = serializers.CharField(write_only=True, required=False)
    data_inicial = serializers.DateField(required=False, allow_null=True)
    data_final = serializers.DateField(required=False, allow_null=True)
    horas_por_dia = serializers.IntegerField(required=False, default=8)


class ProjetoSerializerCreate(serializers.Serializer):
    tecnologias_id = serializers.ListField(
        child=serializers.IntegerField(), write_only=True, required=True
    )
    nome = serializers.CharField(write_only=True, required=False)
    data_inicial = serializers.DateField(required=False, allow_null=True)
    data_final = serializers.DateField(required=False, allow_null=True)
    horas_por_dia = serializers.IntegerField(required=False, default=8)
