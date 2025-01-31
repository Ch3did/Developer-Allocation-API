from drf_spectacular.utils import extend_schema
from rest_framework import status, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from ..models import Technology
from ..serializers import TechnologySerializer, TechnologySerializerUpdate
from .base import CustomPagination


class TechnologiesViewSet(viewsets.ModelViewSet):
    queryset = Technology.objects.all()
    serializer_class = TechnologySerializer
    pagination_class = CustomPagination
    permission_classes = [IsAuthenticated]

    def update(self, request, *args, **kwargs):
        return self._custom_update(request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        return self._custom_update(request, *args, **kwargs)

    @extend_schema(
        summary="Centraliza update do Objeto Alocacao",
        description="",
        request=TechnologySerializerUpdate,
    )
    def _custom_update(self, request, *args, **kwargs):
        serializer = TechnologySerializerUpdate(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data
        technology = Technology.objects.get(id=validated_data["technology_id"])

        technology.name = validated_data.get("name", technology.name)

        technology.save()
        return Response(
            {"message": "Atualizado com sucesso!"}, status=status.HTTP_200_OK
        )
