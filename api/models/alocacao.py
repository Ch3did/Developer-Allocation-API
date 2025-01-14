from django.db import models

from ..models.programador import Programador
from ..models.projeto import Projeto


class Alocacao(models.Model):
    projeto = models.ForeignKey(
        Projeto, on_delete=models.CASCADE, related_name="alocacoes"
    )
    programador = models.ForeignKey(
        Programador, on_delete=models.CASCADE, related_name="alocacoes"
    )
    horas = models.PositiveIntegerField(default=8)

    def __str__(self):
        return f"{self.programador} -> {self.projeto}"
