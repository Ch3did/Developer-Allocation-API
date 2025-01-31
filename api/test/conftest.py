from datetime import date

import pytest
from rest_framework.test import APIClient

from ..models import Developers, Project, Technology


@pytest.fixture
def api_client():
    """
    Retorna um cliente de testes para realizar requisições.
    """
    return APIClient()


@pytest.fixture
def get_jwt(api_client) -> str:
    """responsavel por retornar o jwt"""
    payload = {"username": 123, "password": 123}
    api_client.post("/register/", data=payload)
    response = api_client.post("/token/", data=payload)
    return response.json()["access"]


@pytest.fixture
def dummy_developers_1() -> Developers:
    developers = Developers.objects.create(name="Carlos")
    technology = Technology.objects.create(name="Python")
    developers.technologies.set([technology])
    return developers


@pytest.fixture
def dummy_developers_2() -> Developers:
    developers = Developers.objects.create(name="Joao")
    technology = Technology.objects.create(name="JavaScript")
    developers.technologies.set([technology])
    return developers


@pytest.fixture
def dummy_project_1() -> Project:
    project1 = Project.objects.create(
        name="Project Teste Python",
        data_inicial=date(2025, 1, 1),
        data_final=date(2025, 12, 31),
    )
    technology1 = Technology.objects.create(name="Python")
    technology2 = Technology.objects.create(name="PHP")
    project1.technologies.set([technology1, technology2])
    return project1


@pytest.fixture
def dummy_project_2() -> Project:
    project2 = Project.objects.create(
        name="Project Teste Javascrip",
        data_inicial=date(2025, 6, 1),
        data_final=date(2025, 12, 31),
    )
    technology = Technology.objects.create(name="JavaScript")
    project2.technologies.set([technology])
    return project2
