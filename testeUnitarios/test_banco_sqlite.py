import pytest
from src.services.banco import Banco


@pytest.fixture
def pangare():
    db = Banco("./data/pangare.db", "uip")
    return db


def test_banco_listar_sem_parametro(pangare):
    result = pangare.listar()
    assert type(result) == list


def test_banco_filtro_sem_parametro(pangare):
    result = pangare.filtro()
    assert type(result) == list


def test_banco_filtro_com_parametro(pangare):
    result = pangare.filtro(id=85)
    assert type(result) == list


def test_banco_filtro_com_mais_de_1_parametro(pangare):
    result = pangare.filtro(True, id=85, processados=73763)
    assert type(result) == list


def test_banco_listar_com_parametro(pangare):
    result = pangare.listar("DataHora")
    assert type(result) == list


def test_banco_listar_com_mais_de_1_parametro(pangare):
    result = pangare.listar("id", "DataHora")
    assert type(result) == list
