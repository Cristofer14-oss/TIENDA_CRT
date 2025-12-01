from peewee import *

db = SqliteDatabase('data.db')

class BaseModel(Model):
    class Meta:
        database = db

class Admin(BaseModel):
    username = CharField(unique=True, max_length=20)
    password = CharField(max_length=20)

class Tenis(BaseModel):
    marca = CharField(max_length=30)
    modelo = CharField(max_length=30)
    color = CharField(max_length=20)
    talla = CharField(max_length=5)
    precio = FloatField()

class Cliente(BaseModel):
    nombre = CharField(max_length=50, unique=True)

class Pedido(BaseModel):
    cliente = ForeignKeyField(Cliente, backref="pedidos")
    tenis = ForeignKeyField(Tenis, backref="pedidos")

def crear_tablas():
    with db:
        db.create_tables([Admin, Tenis, Cliente, Pedido])
