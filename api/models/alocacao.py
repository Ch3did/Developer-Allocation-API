from django.db import models
from django.db.models import Sum

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

    def get_horas_alocadas(self, projeto_id) -> int:
        """Busca entre todas as alocacaoes a quantidade de horas ja usadas no projeto"""
        total_horas = Alocacao.objects.filter(projeto=projeto_id).aggregate(
            Sum("horas")
        )
        return total_horas.get("horas__sum", 0) or 0
