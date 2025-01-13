from rest_framework import serializers

from ..models import Projeto, Tecnologia
from .tecnologia_serializer import TecnologiaSerializer


class ProjetoSerializer(serializers.ModelSerializer):
    tecnologias = TecnologiaSerializer(many=True)

    class Meta:
        model = Projeto
        fields = "__all__"

    def create(self, validated_data):
        tecnologias_data = validated_data.pop("tecnologias")
        projeto = Projeto.objects.create(**validated_data)
        for tecnologia_data in tecnologias_data:
            tecnologia, _ = Tecnologia.objects.get_or_create(**tecnologia_data)
            projeto.tecnologias.add(tecnologia)
        return projeto
