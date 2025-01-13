from rest_framework import viewsets

from .models import Alocacao
from .models.programador import Programador
from .models.projeto import Projeto
from .models.tecnologia import Tecnologia
from .serializers import (AlocacaoSerializer, ProgramadorSerializer,
                          ProjetoSerializer, TecnologiaSerializer)


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
