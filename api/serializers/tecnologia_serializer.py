from rest_framework import serializers

from ..models import Tecnologia


class TecnologiaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tecnologia
        fields = "__all__"


class TecnologiaSerializerUpdate(serializers.Serializer):
    tecnologia_id = serializers.IntegerField(write_only=True, required=True)
    nome = serializers.CharField(write_only=True, required=False)
