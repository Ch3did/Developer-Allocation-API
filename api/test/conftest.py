from datetime import date

import pytest
from rest_framework.test import APIClient

from ..models import Programador, Projeto, Tecnologia


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
def dummy_programador_1() -> Programador:
    programador = Programador.objects.create(nome="Carlos")
    tecnologia = Tecnologia.objects.create(nome="Python")
    programador.tecnologias.set([tecnologia])
    return programador


@pytest.fixture
def dummy_programador_2() -> Programador:
    programador = Programador.objects.create(nome="Joao")
    tecnologia = Tecnologia.objects.create(nome="JavaScript")
    programador.tecnologias.set([tecnologia])
    return programador


@pytest.fixture
def dummy_projeto_1() -> Projeto:
    projeto1 = Projeto.objects.create(
        nome="Projeto Teste Python",
        data_inicial=date(2025, 1, 1),
        data_final=date(2025, 12, 31),
    )
    tecnologia1 = Tecnologia.objects.create(nome="Python")
    tecnologia2 = Tecnologia.objects.create(nome="PHP")
    projeto1.tecnologias.set([tecnologia1, tecnologia2])
    return projeto1


@pytest.fixture
def dummy_projeto_2() -> Projeto:
    projeto2 = Projeto.objects.create(
        nome="Projeto Teste Javascrip",
        data_inicial=date(2025, 6, 1),
        data_final=date(2025, 12, 31),
    )
    tecnologia = Tecnologia.objects.create(nome="JavaScript")
    projeto2.tecnologias.set([tecnologia])
    return projeto2
