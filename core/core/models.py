from peewee import *
import datetime

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
    celular = CharField(max_length=20, null=True)

class Pedido(BaseModel):
    cliente = ForeignKeyField(Cliente, backref="pedidos")
    tenis = ForeignKeyField(Tenis, backref="pedidos")
    fecha = DateField(default=datetime.date.today)       
    estado = CharField(default="Pendiente")              
    precio = FloatField(default=0.0)                     


def crear_tablas():
    with db:
        db.create_tables([Admin, Tenis, Cliente, Pedido])

