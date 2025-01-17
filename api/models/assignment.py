from django.db import models
from django.db.models import Sum

from .developers import Developers
from .project import Project


class Assignment(models.Model):
    project = models.ForeignKey(
        Project, on_delete=models.CASCADE, related_name="alocacoes"
    )
    developers = models.ForeignKey(
        Developers, on_delete=models.CASCADE, related_name="alocacoes"
    )
    hours = models.PositiveIntegerField(default=8)

    def __str__(self):
        return f"{self.developers} -> {self.project}"

    def get_hours_alocadas(self, project_id) -> int:
        """Busca entre todas as alocacaoes a quantidade de hours ja usadas no project"""
        total_hours = Assignment.objects.filter(project=project_id).aggregate(
            Sum("hours")
        )
        return total_hours.get("hours__sum", 0) or 0
