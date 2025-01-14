from rest_framework import serializers

from ..models.alocacao import Alocacao


class AlocacaoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Alocacao
        fields = "__all__"


class AlocacaoSerializerCreate(serializers.Serializer):
    projeto_id = serializers.IntegerField(write_only=True, required=True)
    programadores_id = serializers.ListField(
        child=serializers.IntegerField(), write_only=True, required=True
    )
    horas = alocacao_id = serializers.IntegerField(required=False)


class AlocacaoSerializerUpdate(serializers.Serializer):
    alocacao_id = serializers.IntegerField(write_only=True, required=True)
    projeto_id = serializers.IntegerField(write_only=True, required=True)
    programadores_id = serializers.ListField(
        child=serializers.IntegerField(), write_only=True, required=True
    )
    horas = alocacao_id = serializers.IntegerField(required=False)
