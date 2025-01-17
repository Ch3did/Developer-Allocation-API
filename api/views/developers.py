from drf_spectacular.utils import extend_schema
from rest_framework import status, viewsets
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from ..models import Developers, Technology
from ..serializers import (DevelopersSerializer, DevelopersSerializerCreate,
                           DevelopersSerializerUpdate)
from .base import CustomPagination


class DevelopersViewSet(viewsets.ModelViewSet):
    queryset = Developers.objects.all()
    serializer_class = DevelopersSerializer
    pagination_class = CustomPagination
    permission_classes = [IsAuthenticated]

    @extend_schema(
        summary="Cria Objeto Alocacao",
        description="",
        request=DevelopersSerializerCreate,
    )
    def create(self, request, *args, **kwargs):
        serializer = DevelopersSerializerCreate(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data

        try:
            technologies = self._validar_technologies(
                validated_data.get("technologies_id", [])
            )
        except ValidationError as e:
            return Response({"error": e.args[0]}, status=status.HTTP_400_BAD_REQUEST)

        developer = Developers.objects.create(
            name=validated_data["name"],
        )

        developer.technologies.set(technologies)
        developer.save()

        return Response(
            {"message": "developer criado com sucesso!"},
            status=status.HTTP_201_CREATED,
        )

    def update(self, request, *args, **kwargs):
        return self._custom_update(request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        return self._custom_update(request, *args, **kwargs)

    @extend_schema(
        summary="Centraliza update do Objeto Alocacao",
        description="",
        request=DevelopersSerializerUpdate,
    )
    def _custom_update(self, request, *args, **kwargs):
        serializer = DevelopersSerializerUpdate(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data
        developer = Developers.objects.get(id=validated_data["developer_id"])
        technologies_data = validated_data["technologies_id"]

        try:
            technologies = self._validar_technologies(technologies_data)
        except ValidationError as e:
            return Response({"error": e.args[0]}, status=status.HTTP_400_BAD_REQUEST)

        if technologies_data:
            developer.technologies.clear()

            for technology in technologies:
                developer.technologies.add(technology)

        developer.name = validated_data.get("name", developer.name)

        developer.save()
        return Response(
            {"message": "Atualizado com sucesso!"}, status=status.HTTP_200_OK
        )

    def _validar_technologies(self, technologies_data):
        technologies = []
        for id_technology in technologies_data:
            try:
                technology = Technology.objects.get(id=id_technology)
                technologies.append(Technology)
            except technology.DoesNotExist:
                raise ValidationError(
                    f"Technology com ID {id_technology} não encontrada."
                )
        return technologies
