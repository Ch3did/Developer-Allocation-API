from drf_spectacular.utils import extend_schema
from rest_framework import status, viewsets
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from ..models import Project, Technology
from ..serializers import (ProjectSerializer, ProjectSerializerCreate,
                           ProjectSerializerUpdate)
from .base import CustomPagination


class ProjectsViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    pagination_class = CustomPagination
    permission_classes = [IsAuthenticated]

    @extend_schema(
        summary="Cria Objeto Alocacao",
        description="",
        request=ProjectSerializerCreate,
    )
    def create(self, request, *args, **kwargs):
        serializer = ProjectSerializerCreate(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data

        try:
            technologies = self._validar_technologies(
                validated_data.get("technologies_id", [])
            )
        except ValidationError as e:
            return Response({"error": e.args[0]}, status=status.HTTP_400_BAD_REQUEST)

        project = Project.objects.create(
            name=validated_data["name"],
            data_inicial=validated_data["data_inicial"],
            data_final=validated_data["data_final"],
            hours_por_dia=validated_data["hours_por_dia"],
        )

        project.technologies.set(technologies)
        project.save()

        return Response(
            {"message": "Project criado com sucesso!"},
            status=status.HTTP_201_CREATED,
        )

    def update(self, request, *args, **kwargs):
        return self._custom_update(request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        return self._custom_update(request, *args, **kwargs)

    @extend_schema(
        summary="Centraliza update do Objeto Alocacao",
        description="",
        request=ProjectSerializerUpdate,
    )
    def _custom_update(self, request, *args, **kwargs):
        serializer = ProjectSerializerUpdate(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data

        project = Project.objects.get(id=validated_data.get("project_id"))

        technologies_data = validated_data["technologies_id"]
        try:
            technologies = self._validar_technologies(technologies_data)
        except ValidationError as e:
            return Response({"error": e.args[0]}, status=status.HTTP_400_BAD_REQUEST)

        if technologies_data:
            Project.technologies.clear()

            for technology in technologies:
                Project.technologies.add(technology)

        project.data_inicial = validated_data.get("data_inicial", project.data_inicial)
        project.data_final = validated_data.get("data_final", project.data_final)
        project.hours_por_dia = validated_data.get(
            "hours_por_dia", project.hours_por_dia
        )

        # TODO: add validacao caso exista alocacao pro project,
        # validar se as hours alocadas n vao estourar

        project.save()

        return Response(
            {"message": "Atualizado com sucesso!"}, status=status.HTTP_200_OK
        )

    def _validar_technologies(self, technologies_data):
        technologies = []
        for id_technology in technologies_data:
            try:
                technology = Technology.objects.get(id=id_technology)
                technologies.append(technology)
            except Technology.DoesNotExist:
                raise ValidationError(
                    f"Technology com ID {id_technology} não encontrada."
                )
        return technologies
