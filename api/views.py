from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination

from .models import Alocacao, Programador, Projeto, Tecnologia
from .serializers import (AlocacaoSerializer, ProgramadorSerializer,
                          ProjetoSerializer, TecnologiaSerializer)


class CustomPagination(PageNumberPagination):
    page_size = 5
    page_size_query_param = "page_size"
    max_page_size = 100


class TecnologiaViewSet(viewsets.ModelViewSet):
    queryset = Tecnologia.objects.all()
    serializer_class = TecnologiaSerializer
    pagination_class = CustomPagination


class ProgramadorViewSet(viewsets.ModelViewSet):
    queryset = Programador.objects.all()
    serializer_class = ProgramadorSerializer
    pagination_class = CustomPagination


class ProjetoViewSet(viewsets.ModelViewSet):
    queryset = Projeto.objects.all()
    serializer_class = ProjetoSerializer
    pagination_class = CustomPagination


class AlocacaoViewSet(viewsets.ModelViewSet):
    queryset = Alocacao.objects.all()
    serializer_class = AlocacaoSerializer
    pagination_class = CustomPagination
