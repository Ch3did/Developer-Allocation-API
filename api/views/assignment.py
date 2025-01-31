from drf_spectacular.utils import extend_schema
from rest_framework import status, viewsets
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from ..models import Assignment, Developers, Project
from ..serializers import (AssignmentSerializer, AssignmentSerializerCreate,
                           AssignmentSerializerUpdate)
from .base import CustomPagination


class AssignmentViewSet(viewsets.ModelViewSet):
    queryset = Assignment.objects.all()
    serializer_class = AssignmentSerializer
    pagination_class = CustomPagination
    permission_classes = [IsAuthenticated]

    @extend_schema(
        summary="Cria Objeto Assignment",
        description="",
        request=AssignmentSerializerCreate,
    )
    def create(self, request, *args, **kwargs):
        serializer = AssignmentSerializerCreate(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data

        try:
            developer = self._validar_developer(validated_data.get("developer_id"))
            project = self._validar_project(validated_data["project_id"])

            self._validar_technologies_no_project(project, developer)

            assignment = Assignment.objects.create(project=project, developer=developer)

            if hours := validated_data.get("hours"):
                assignment.hours = hours

            self._validar_hours(assignment)

        except ValidationError as e:
            return Response({"error": e.args[0]}, status=status.HTTP_400_BAD_REQUEST)

        assignment.save()

        return Response(
            {"message": "Alocação criada com sucesso!"},
            status=status.HTTP_201_CREATED,
        )

    def update(self, request, *args, **kwargs):
        return self._custom_update(request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        return self._custom_update(request, *args, **kwargs)

    @extend_schema(
        summary="Centraliza update do Objeto Assignment",
        description="",
        request=AssignmentSerializerUpdate,
    )
    def _custom_update(self, request, *args, **kwargs):
        serializer = AssignmentSerializerUpdate(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data

        try:
            assignment = self._validar_assignment(validated_data.get("assignment_id"))

            if developer_id := validated_data.get("developer_id"):
                developer = self._validar_developer(developer_id)
                assignment.developer = developer

            if project_id := validated_data.get("project_id"):
                project = self._validar_project(project_id)
                assignment.project = project

            if hours := validated_data.get("hours"):
                assignment.hours = hours
                self._validar_hours(hours, assignment)

            self._validar_technologies_no_project(
                assignment.project, assignment.developer
            )

        except ValidationError as e:
            return Response({"error": e.args[0]}, status=status.HTTP_400_BAD_REQUEST)

        assignment.save()

        return Response(
            {"message": "Alocação atualizada com sucesso!"},
            status=status.HTTP_200_OK,
        )

    def _validar_assignment(self, assignment_id: int) -> Assignment | Exception:
        try:
            assignment = Assignment.objects.get(id=assignment_id)
        except Assignment.DoesNotExist:
            raise ValidationError(f"Assignment com ID {assignment_id} não encontrada.")
        return assignment

    def _validar_developer(self, id_developer: int) -> Developers | Exception:
        """Valida developer existe"""
        try:
            developer = Developers.objects.get(id=id_developer)
        except Developers.DoesNotExist:
            raise ValidationError(f"Developer com ID {id_developer} não encontrada.")
        return developer

    def _validar_project(self, project_id: int) -> Project | Exception:
        """Valida project existe"""
        try:
            project = Project.objects.get(id=project_id)
        except project.DoesNotExist:
            raise ValidationError(f"Project com ID {project_id} não encontrada.")
        return project

    def _validar_hours(self, assignment: Assignment) -> None | Exception:
        """Compara as hours alocadas + novas hours com o limite do project"""
        total_hours = assignment.project.get_total_hours()
        hours_alocadas = assignment.get_hours_alocadas(assignment.project.id)

        if total_hours < (hours_alocadas + assignment.hours):
            raise ValidationError(
                f"""As novas hours alocadas excedem o limite para o
                project em {(hours_alocadas + assignment.hours)-total_hours}."""
            )

    def _validar_technologies_no_project(
        self, project: Project, developer: Developers
    ) -> None | Exception:
        """Função para verificar se ao menos uma tecnologia
        do pDeveloper está associada ao project.
        """
        developers_tech = developer.technologies.all()

        for tecnologia in developers_tech:
            if project.technologies.filter(name=tecnologia.name):
                return

        raise ValidationError(
            f"""{developer.name} não possui as technologies
            necessárias para ser alocado neste project."""
        )
