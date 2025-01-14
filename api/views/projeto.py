from drf_spectacular.utils import extend_schema
from rest_framework import status, viewsets
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

from api.views.pagination import CustomPagination

from ..models import Projeto, Tecnologia
from ..serializers import (ProjetoSerializer, ProjetoSerializerCreate,
                           ProjetoSerializerUpdate)


class ProjetoViewSet(viewsets.ModelViewSet):
    queryset = Projeto.objects.all()
    serializer_class = ProjetoSerializer
    pagination_class = CustomPagination

    @extend_schema(
        summary="Cria Objeto Alocacao",
        description="",
        request=ProjetoSerializerCreate,
    )
    def create(self, request, *args, **kwargs):
        serializer = ProjetoSerializerCreate(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data

        try:
            tecnologias = self._validar_tecnologias(
                validated_data.get("tecnologias_id", [])
            )
        except ValidationError as e:
            return Response({"error": e.args[0]}, status=status.HTTP_400_BAD_REQUEST)

        programador = Projeto.objects.create(
            nome=validated_data["nome"],
            data_inicial=validated_data["data_inicial"],
            data_final=validated_data["data_final"],
            horas_por_dia=validated_data["horas_por_dia"],
        )

        programador.tecnologias.set(tecnologias)
        programador.save()

        return Response(
            {"message": "Programador criado com sucesso!"},
            status=status.HTTP_201_CREATED,
        )

    def update(self, request, *args, **kwargs):
        return self._custom_update(request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        return self._custom_update(request, *args, **kwargs)

    @extend_schema(
        summary="Centraliza update do Objeto Alocacao",
        description="",
        request=ProjetoSerializerUpdate,
    )
    def _custom_update(self, request, *args, **kwargs):
        serializer = ProjetoSerializerUpdate(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data

        projeto = Projeto.objects.get(id=validated_data.get("projeto_id"))

        tecnologias_data = validated_data["tecnologias_id"]
        try:
            tecnologias = self._validar_tecnologias(tecnologias_data)
        except ValidationError as e:
            return Response({"error": e.args[0]}, status=status.HTTP_400_BAD_REQUEST)

        if tecnologias_data:
            Projeto.tecnologias.clear()

            for tecnologia in tecnologias:
                Projeto.tecnologias.add(tecnologia)

        projeto.data_inicial = validated_data.get("data_inicial", projeto.data_inicial)
        projeto.data_final = validated_data.get("data_final", projeto.data_final)
        projeto.horas_por_dia = validated_data.get(
            "horas_por_dia", projeto.horas_por_dia
        )

        # TODO: add validacao caso exista alocacao pro projeto, validar se as horas alocadas n vao estourar

        projeto.save()

        return Response(
            {"message": "Atualizado com sucesso!"}, status=status.HTTP_200_OK
        )

    def _validar_tecnologias(self, tecnologias_data):
        tecnologias = []
        for id_tecnologia in tecnologias_data:
            try:
                tecnologia = Tecnologia.objects.get(id=id_tecnologia)
                tecnologias.append(tecnologia)
            except Tecnologia.DoesNotExist:
                raise ValidationError(
                    f"Tecnologia com ID {id_tecnologia} não encontrada."
                )
        return tecnologias
