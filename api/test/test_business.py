import pytest


@pytest.mark.django_db
def test_alocacao_technologies_iguais_201(
    api_client, dummy_developer_1, dummy_project_1, get_jwt
):
    """Valida a criação de uma alocação com technologies compatíveis retorna 201"""
    headers = {
        "Authorization": f"Bearer {get_jwt}",
    }

    payload = {
        "project_id": dummy_project_1.id,
        "developer_id": [dummy_developer_1.id],
        "hours": 8,
    }

    response = api_client.post("/api/alocacoes/", data=payload, headers=headers)

    assert response.status_code == 201


@pytest.mark.django_db
def test_alocacao_technologies_diferentes_400(
    api_client, dummy_developer_1, dummy_project_2, get_jwt
):
    """Valida se uma requisição com technologies distintas retorna erro 400"""
    headers = {
        "Authorization": f"Bearer {get_jwt}",
    }

    payload = {
        "project_id": dummy_project_2.id,
        "developer_id": [dummy_developer_1.id],
        "hours": 8,
    }

    response = api_client.post("/api/alocacoes/", data=payload, headers=headers)

    assert response.status_code == 400


@pytest.mark.django_db
def test_alocacao_hours_excedentes_400(
    api_client, dummy_developer_1, dummy_project_2, get_jwt
):
    """Valida se uma requisição com hours excedentes retorna erro 400"""

    headers = {
        "Authorization": f"Bearer {get_jwt}",
    }

    payload = {
        "project_id": dummy_project_2.id,
        "developer_id": [dummy_developer_1.id],
        "hours": 1000,
    }

    response = api_client.post("/api/alocacoes/", data=payload, headers=headers)

    assert response.status_code == 400
