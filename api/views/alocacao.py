from drf_spectacular.utils import extend_schema
from rest_framework import status, viewsets
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from ..views.base  import CustomPagination

from ..models import Alocacao, Programador, Projeto
from ..serializers import (AlocacaoSerializer, AlocacaoSerializerCreate,
                           AlocacaoSerializerUpdate)


class AlocacaoViewSet(viewsets.ModelViewSet):
    queryset = Alocacao.objects.all()
    serializer_class = AlocacaoSerializer
    pagination_class = CustomPagination
    permission_classes = [IsAuthenticated]

    @extend_schema(
        summary="Cria Objeto Alocacao",
        description="",
        request=AlocacaoSerializerCreate,
    )
    def create(self, request, *args, **kwargs):
        serializer = AlocacaoSerializerCreate(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data

        try:
            programadores = self._validar_programadores(
                validated_data.get("programadores_id", [])
            )
            projeto = self._validar_projeto(validated_data["projeto_id"])

            alocacao = Alocacao.objects.create(
                projeto=projeto,
            )

            if horas := validated_data.get("horas"):
                alocacao.horas = horas

            self._validar_horas(alocacao.horas, programadores, projeto)

        except ValidationError as e:
            return Response({"error": e.args[0]}, status=status.HTTP_400_BAD_REQUEST)

        alocacao.programador.set(programadores)
        alocacao.save()

        return Response(
            {"message": "Alocação criada com sucesso!"},
            status=status.HTTP_201_CREATED,
        )

    def update(self, request, *args, **kwargs):
        return self._custom_update(request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        return self._custom_update(request, *args, **kwargs)

    @extend_schema(
        summary="Centraliza update do Objeto Alocacao",
        description="",
        request=AlocacaoSerializerUpdate,
    )
    def _custom_update(self, request, *args, **kwargs):
        serializer = AlocacaoSerializerUpdate(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data

        try:
            alocacao = Alocacao.objects.get(id=validated_data["alocacao_id"])
        except Alocacao.DoesNotExist:
            return Response(
                {
                    "error": f"""Alocação com ID {validated_data['alocacao_id']}
                    não encontrada."""
                },
                status=status.HTTP_404_NOT_FOUND,
            )

        try:
            programadores = self._validar_programadores(
                validated_data.get("programadores_id", [])
            )
            projeto = self._validar_projeto(validated_data["projeto_id"])
        except ValidationError as e:
            return Response({"error": e.args[0]}, status=status.HTTP_400_BAD_REQUEST)

        if "horas" in validated_data:
            horas = validated_data["horas"]
            self._validar_horas(horas, programadores, projeto)
            alocacao.horas = horas

        alocacao.projeto = projeto
        alocacao.programador.set(programadores)
        alocacao.save()

        return Response(
            {"message": "Alocação atualizada com sucesso!"},
            status=status.HTTP_200_OK,
        )

    def _validar_programadores(self, programadores_data):
        tecnologias = []
        for id_programador in programadores_data:
            try:
                tecnologia = Programador.objects.get(id=id_programador)
                tecnologias.append(tecnologia)
            except Programador.DoesNotExist:
                raise ValidationError(
                    f"Programador com ID {id_programador} não encontrada."
                )
        return tecnologias

    def _validar_projeto(self, projeto_id):
        try:
            projeto = Projeto.objects.get(id=projeto_id)
        except projeto.DoesNotExist:
            raise ValidationError(f"Projeto com ID {projeto_id} não encontrada.")
        return projeto

    def _validar_horas(self, horas, programadores, projeto):
        if horas <= (projeto.horas_por_dia * len(programadores)):
            return Response(
                {
                    "error": """As horas alocadas por desenvolvedor
                    excedem o limite projeto."""
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
