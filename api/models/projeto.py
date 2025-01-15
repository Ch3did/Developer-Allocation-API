from django.db import models

from .tecnologia import Tecnologia


class Projeto(models.Model):
    nome = models.CharField(max_length=100)
    data_inicial = models.DateField()
    data_final = models.DateField()
    tecnologias = models.ManyToManyField(Tecnologia, related_name="projetos")

    def __str__(self):
        return self.nome

    def get_total_horas(self) -> int:
        """Considera 8 horas tempo maximo por dia"""
        delta = self.data_final - self.data_inicial
        total_horas_projeto = delta.days * 8
        return total_horas_projeto
