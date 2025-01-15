from drf_spectacular.utils import extend_schema
from rest_framework import status, viewsets
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from ..views.base  import CustomPagination

from ..models import Programador, Tecnologia
from ..serializers import (ProgramadorSerializer, ProgramadorSerializerCreate,
                           ProgramadorSerializerUpdate)


class ProgramadorViewSet(viewsets.ModelViewSet):
    queryset = Programador.objects.all()
    serializer_class = ProgramadorSerializer
    pagination_class = CustomPagination
    authentication_classes = [IsAuthenticated]

    @extend_schema(
        summary="Cria Objeto Alocacao",
        description="",
        request=ProgramadorSerializerCreate,
    )
    def create(self, request, *args, **kwargs):
        serializer = ProgramadorSerializerCreate(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data

        try:
            tecnologias = self._validar_tecnologias(
                validated_data.get("tecnologias_id", [])
            )
        except ValidationError as e:
            return Response({"error": e.args[0]}, status=status.HTTP_400_BAD_REQUEST)

        programador = Programador.objects.create(
            nome=validated_data["nome"],
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
        request=ProgramadorSerializerUpdate,
    )
    def _custom_update(self, request, *args, **kwargs):
        serializer = ProgramadorSerializerUpdate(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data
        programador = Programador.objects.get(id=validated_data["programador_id"])
        tecnologias_data = validated_data["tecnologias_id"]

        try:
            tecnologias = self._validar_tecnologias(tecnologias_data)
        except ValidationError as e:
            return Response({"error": e.args[0]}, status=status.HTTP_400_BAD_REQUEST)

        if tecnologias_data:
            programador.tecnologias.clear()

            for tecnologia in tecnologias:
                programador.tecnologias.add(tecnologia)

        programador.nome = validated_data.get("nome", programador.nome)

        programador.save()
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
