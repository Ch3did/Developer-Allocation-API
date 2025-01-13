from rest_framework import serializers

from ..models import Programador, Tecnologia
from .tecnologia_serializer import TecnologiaSerializer


class ProgramadorSerializer(serializers.ModelSerializer):
    tecnologias = TecnologiaSerializer(many=True)

    class Meta:
        model = Programador
        fields = "__all__"

    def create(self, validated_data):
        tecnologias_data = validated_data.pop("tecnologias")
        programador = Programador.objects.create(**validated_data)
        for tecnologia_data in tecnologias_data:
            tecnologia, _ = Tecnologia.objects.get_or_create(**tecnologia_data)
            programador.tecnologias.add(tecnologia)
        return programador

    def update(self, instance, validated_data):
        tecnologias_data = validated_data.pop("tecnologias")
        instance.nome = validated_data.get("nome", instance.nome)
        instance.tecnologias.clear()
        for tecnologia_data in tecnologias_data:
            tecnologia, _ = Tecnologia.objects.get_or_create(**tecnologia_data)
            instance.tecnologias.add(tecnologia)
        instance.save()
        return instance
