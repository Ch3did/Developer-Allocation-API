from django.contrib import admin

from .models import Assignment, Developers, Project, Technology


@admin.register(Technology)
class TechnologyAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    search_fields = ("name",)
    ordering = ("name",)


@admin.register(Developers)
class DevelopersAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    search_fields = ("name",)
    filter_horizontal = ("technologies",)


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "data_inicial", "data_final")
    search_fields = ("name",)
    list_filter = ("data_inicial", "data_final")
    filter_horizontal = ("technologies",)


@admin.register(Assignment)
class AssignmentAdmin(admin.ModelAdmin):
    list_display = ("id", "project", "developer", "hours")
    search_fields = ("project__name", "developer__name")
    list_filter = ("project", "developer")
