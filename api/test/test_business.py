import pytest


@pytest.mark.django_db
def test_alocacao_tecnologias_iguais_201(
    api_client, dummy_programador_1, dummy_projeto_1, get_jwt
):
    """Valida a criação de uma alocação com tecnologias compatíveis retorna 201"""
    headers = {
        "Authorization": f"Bearer {get_jwt}",
    }

    payload = {
        "projeto_id": dummy_projeto_1.id,
        "programador_id": [dummy_programador_1.id],
        "horas": 8,
    }

    response = api_client.post("/api/alocacoes/", data=payload, headers=headers)

    assert response.status_code == 201


@pytest.mark.django_db
def test_alocacao_tecnologias_diferentes_400(
    api_client, dummy_programador_1, dummy_projeto_2, get_jwt
):
    """Valida se uma requisição com tecnologias distintas retorna erro 400"""
    headers = {
        "Authorization": f"Bearer {get_jwt}",
    }

    payload = {
        "projeto_id": dummy_projeto_2.id,
        "programador_id": [dummy_programador_1.id],
        "horas": 8,
    }

    response = api_client.post("/api/alocacoes/", data=payload, headers=headers)

    assert response.status_code == 400


@pytest.mark.django_db
def test_alocacao_horas_excedentes_400(
    api_client, dummy_programador_1, dummy_projeto_2, get_jwt
):
    """Valida se uma requisição com horas excedentes retorna erro 400"""

    headers = {
        "Authorization": f"Bearer {get_jwt}",
    }

    payload = {
        "projeto_id": dummy_projeto_2.id,
        "programador_id": [dummy_programador_1.id],
        "horas": 1000,
    }

    response = api_client.post("/api/alocacoes/", data=payload, headers=headers)

    assert response.status_code == 400
