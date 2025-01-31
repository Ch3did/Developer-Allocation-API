from django.db import models

from .technology import Technology


class Project(models.Model):
    name = models.CharField(max_length=100)
    data_inicial = models.DateField()
    data_final = models.DateField()
    technologies = models.ManyToManyField(Technology, related_name="projects")

    def __str__(self):
        return self.name

    def get_total_hours(self) -> int:
        """Considera 8 hours tempo maximo por dia"""
        delta = self.data_final - self.data_inicial
        total_hours_project = delta.days * 8
        return total_hours_project
