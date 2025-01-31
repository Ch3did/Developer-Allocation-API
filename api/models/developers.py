from django.db import models

from .technology import Technology


class Developers(models.Model):
    name = models.CharField(max_length=100)
    technologies = models.ManyToManyField(Technology, related_name="developers")

    def __str__(self):
        return self.name
