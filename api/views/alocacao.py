from drf_spectacular.utils import extend_schema
from rest_framework import status, viewsets
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from ..models import Alocacao, Programador, Projeto
from ..serializers import (AlocacaoSerializer, AlocacaoSerializerCreate,
                           AlocacaoSerializerUpdate)
from ..views.base import CustomPagination


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
            programador = self._validar_programador(
                validated_data.get("programador_id")
            )
            projeto = self._validar_projeto(validated_data["projeto_id"])

            alocacao = Alocacao.objects.create(projeto=projeto, programador=programador)

            if horas := validated_data.get("horas"):
                alocacao.horas = horas

            self._validar_horas(alocacao)

        except ValidationError as e:
            return Response({"error": e.args[0]}, status=status.HTTP_400_BAD_REQUEST)

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
            alocacao = self._validar_alocacao(validated_data.get("alocacao_id"))

            if programador_id := validated_data.get("programador_id"):
                programador = self._validar_programador(programador_id)
                alocacao.programador = programador

            if projeto_id := validated_data.get("projeto_id"):
                projeto = self._validar_projeto(projeto_id)
                alocacao.projeto = projeto

            if horas := validated_data.get("horas"):
                alocacao.horas = horas
                self._validar_horas(horas, alocacao)

        except ValidationError as e:
            return Response({"error": e.args[0]}, status=status.HTTP_400_BAD_REQUEST)

        alocacao.save()

        return Response(
            {"message": "Alocação atualizada com sucesso!"},
            status=status.HTTP_200_OK,
        )

    def _validar_alocacao(self, alocacao_id: int) -> Alocacao | Exception:
        try:
            alocacao = Alocacao.objects.get(id=alocacao_id)
        except Alocacao.DoesNotExist:
            raise ValidationError(f"Alocacao com ID {alocacao_id} não encontrada.")
        return alocacao

    def _validar_programador(self, id_programador: int) -> Programador | Exception:
        """Valida programador existe"""
        try:
            programador = Programador.objects.get(id=id_programador)
        except Programador.DoesNotExist:
            raise ValidationError(
                f"Programador com ID {id_programador} não encontrada."
            )
        return programador

    def _validar_projeto(self, projeto_id: int) -> Projeto | Exception:
        """Valida projeto existe"""
        try:
            projeto = Projeto.objects.get(id=projeto_id)
        except projeto.DoesNotExist:
            raise ValidationError(f"Projeto com ID {projeto_id} não encontrada.")
        return projeto

    def _validar_horas(self, alocacao: Alocacao) -> None | Exception:
        """Compara as horas alocadas + novas horas com o limite do projeto"""
        total_horas = alocacao.projeto.get_total_horas()
        horas_alocadas = alocacao.get_horas_alocadas(alocacao.projeto.id)

        if total_horas < (horas_alocadas + alocacao.horas):
            raise ValidationError(
                f"""As novas horas alocadas excedem o limite para o
                projeto em {(horas_alocadas + alocacao.horas)-total_horas}."""
            )
