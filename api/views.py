from rest_framework import viewsets

from api.serializers.serializer import (
    AlocacaoSerializer,
    ProgramadorSerializer,
    ProjetoSerializer,
    TecnologiaSerializer,
)

from .models import Alocacao
from .models.programador import Programador
from .models.projeto import Projeto
from .models.tecnologia import Tecnologia


class TecnologiaViewSet(viewsets.ModelViewSet):
    queryset = Tecnologia.objects.all()
    serializer_class = TecnologiaSerializer


class ProgramadorViewSet(viewsets.ModelViewSet):
    queryset = Programador.objects.all()
    serializer_class = ProgramadorSerializer


class ProjetoViewSet(viewsets.ModelViewSet):
    queryset = Projeto.objects.all()
    serializer_class = ProjetoSerializer


class AlocacaoViewSet(viewsets.ModelViewSet):
    queryset = Alocacao.objects.all()
    serializer_class = AlocacaoSerializer
