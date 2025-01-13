from django.contrib import admin

from .models import Alocacao, Programador, Projeto, Tecnologia


@admin.register(Tecnologia)
class TecnologiaAdmin(admin.ModelAdmin):
    list_display = ("id", "nome")
    search_fields = ("nome",)
    ordering = ("nome",)


@admin.register(Programador)
class ProgramadorAdmin(admin.ModelAdmin):
    list_display = ("id", "nome")
    search_fields = ("nome",)
    filter_horizontal = ("tecnologias",)


@admin.register(Projeto)
class ProjetoAdmin(admin.ModelAdmin):
    list_display = ("id", "nome", "data_inicial", "data_final")
    search_fields = ("nome",)
    list_filter = ("data_inicial", "data_final")
    filter_horizontal = ("tecnologias",)


@admin.register(Alocacao)
class AlocacaoAdmin(admin.ModelAdmin):
    list_display = ("id", "projeto", "programador", "horas")
    search_fields = ("projeto__nome", "programador__nome")
    list_filter = ("projeto", "programador")
