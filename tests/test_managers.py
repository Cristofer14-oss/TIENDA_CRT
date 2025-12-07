import sys, os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

import pytest
from peewee import SqliteDatabase
from core.models import Admin, Tenis, Cliente, Pedido
from core import managers

# -------------------------------
# BD TEMPORAL PARA PRUEBAS
# -------------------------------
test_db = SqliteDatabase(":memory:")

MODELS = [Admin, Tenis, Cliente, Pedido]

@pytest.fixture(scope="function", autouse=True)
def db_setup():
    """Crear BD temporal antes de cada prueba"""
    test_db.bind(MODELS, bind_refs=False, bind_backrefs=False)
    test_db.connect()
    test_db.create_tables(MODELS)
    yield
    test_db.drop_tables(MODELS)
    test_db.close()


# -------------------------------
# TEST: ADMIN
# -------------------------------
def test_crear_admin():
    admin = managers.crear_admin("admin1", "12345")
    assert admin.username == "admin1"
    assert Admin.select().count() == 1


def test_verificar_admin():
    managers.crear_admin("cris", "14253")
    ok = managers.verificar_admin("cris", "14253")
    assert ok is not None

    fail = managers.verificar_admin("cris", "00000")
    assert fail is None


# -------------------------------
# TEST: TENIS
# -------------------------------
def test_agregar_tenis():
    tenis = managers.agregar_tenis("Nike", "Air Max", "Negro", "42", 799)
    assert tenis.marca == "Nike"
    assert Tenis.select().count() == 1


def test_listar_tenis():
    managers.agregar_tenis("Adidas", "Forum", "Blanco", "40", 650)
    lista = list(managers.listar_tenis())
    assert len(lista) == 1


def test_eliminar_tenis():
    t = managers.agregar_tenis("Puma", "RS-X", "Rojo", "41", 720)
    eliminado = managers.eliminar_tenis(t.id)
    assert eliminado is True
    assert Tenis.select().count() == 0


# -------------------------------
# TEST: CLIENTE
# -------------------------------
def test_obtener_o_crear_cliente():
    c1 = managers.obtener_o_crear_cliente("Luis")
    assert c1.nombre == "Luis"
    assert Cliente.select().count() == 1

    # Llamar de nuevo no crea otro
    c2 = managers.obtener_o_crear_cliente("Luis")
    assert Cliente.select().count() == 1
    assert c1.id == c2.id


# -------------------------------
# TEST: PEDIDOS
# -------------------------------
def test_hacer_pedido():
    cliente = managers.obtener_o_crear_cliente("Ana")
    tenis = managers.agregar_tenis("Nike", "Dunk", "Azul", "39", 900)

    ok, msg = managers.hacer_pedido(cliente, tenis.id, "77788899")

    assert ok is True
    assert "Pedido registrado" in msg
    assert Pedido.select().count() == 1

    pedido = Pedido.get()
    assert pedido.cliente.nombre == "Ana"
    assert pedido.tenis.id == tenis.id
    assert pedido.estado == "Pendiente"


def test_hacer_pedido_no_existe():
    cliente = managers.obtener_o_crear_cliente("Carlos")

    ok, msg = managers.hacer_pedido(cliente, 9999, "77744400")

    assert ok is False
    assert "Tenis no encontrado" in msg
    assert Pedido.select().count() == 0


def test_listar_pedidos():
    cliente = managers.obtener_o_crear_cliente("Luisa")
    tenis = managers.agregar_tenis("Jordan", "1 Retro", "Negro", "42", 1200)

    managers.hacer_pedido(cliente, tenis.id, "70011223")

    pedidos = list(managers.listar_pedidos())
    assert len(pedidos) == 1
