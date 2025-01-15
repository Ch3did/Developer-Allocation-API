from drf_spectacular.utils import extend_schema
from rest_framework import status, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from ..views.base  import CustomPagination

from ..models import Tecnologia
from ..serializers import TecnologiaSerializer, TecnologiaSerializerUpdate


class TecnologiaViewSet(viewsets.ModelViewSet):
    queryset = Tecnologia.objects.all()
    serializer_class = TecnologiaSerializer
    pagination_class = CustomPagination
    permission_classes = [IsAuthenticated]

    def update(self, request, *args, **kwargs):
        return self._custom_update(request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        return self._custom_update(request, *args, **kwargs)

    @extend_schema(
        summary="Centraliza update do Objeto Alocacao",
        description="",
        request=TecnologiaSerializerUpdate,
    )
    def _custom_update(self, request, *args, **kwargs):
        serializer = TecnologiaSerializerUpdate(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data
        tecnologia = Tecnologia.objects.get(id=validated_data["tecnologia_id"])

        tecnologia.nome = validated_data.get("nome", tecnologia.nome)

        tecnologia.save()
        return Response(
            {"message": "Atualizado com sucesso!"}, status=status.HTTP_200_OK
        )
