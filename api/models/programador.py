from django.db import models

from .tecnologia import Tecnologia


class Programador(models.Model):
    nome = models.CharField(max_length=100)
    tecnologias = models.ManyToManyField(Tecnologia, related_name="programadores")

    def __str__(self):
        return self.nome
