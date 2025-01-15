from rest_framework import serializers

from ..models.alocacao import Alocacao


class AlocacaoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Alocacao
        fields = "__all__"


class AlocacaoSerializerCreate(serializers.Serializer):
    projeto_id = serializers.IntegerField(write_only=True, required=True)
    programador_id = serializers.IntegerField(required=False)
    horas = alocacao_id = serializers.IntegerField(required=False)


class AlocacaoSerializerUpdate(serializers.Serializer):
    alocacao_id = serializers.IntegerField(write_only=True, required=False)
    projeto_id = serializers.IntegerField(write_only=True, required=False)
    programador_id = serializers.IntegerField(required=False)
    horas = alocacao_id = serializers.IntegerField(required=False)
