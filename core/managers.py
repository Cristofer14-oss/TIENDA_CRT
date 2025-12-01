from core.models import Admin, Tenis, Cliente, Pedido, crear_tablas

# Inicializar BD
crear_tablas()

# --- ADMIN ---
def verificar_admin(username, password):
    return Admin.get_or_none(Admin.username == username, Admin.password == password)

def crear_admin(username, password):
    return Admin.create(username=username, password=password)

# --- TENIS ---
def agregar_tenis(marca, modelo, color, talla, precio):
    return Tenis.create(marca=marca, modelo=modelo, color=color, talla=talla, precio=precio)

def listar_tenis():
    return Tenis.select()

def eliminar_tenis(tenis_id):
    tenis = Tenis.get_or_none(Tenis.id == tenis_id)
    if tenis:
        tenis.delete_instance()
        return True
    return False

# --- CLIENTE ---
def obtener_o_crear_cliente(nombre):
    cliente, creado = Cliente.get_or_create(nombre=nombre)
    return cliente

# --- PEDIDOS ---
def hacer_pedido(cliente, tenis_id):
    tenis = Tenis.get_or_none(Tenis.id == tenis_id)
    if not tenis:
        return False, "⚠️ Tenis no encontrado"
    Pedido.create(cliente=cliente, tenis=tenis)
    return True, f"✅ Pedido registrado: {tenis.marca} {tenis.modelo}"

def listar_pedidos():
    return Pedido.select()
