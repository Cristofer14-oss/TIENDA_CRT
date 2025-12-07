import os
from core import managers
from getpass import getpass

# Función para limpiar pantalla (compatible con Windows y Linux)
def limpiar():
    os.system("cls" if os.name == "nt" else "clear")

def menu_principal():
    while True:
        limpiar()
        print("\n= = = = = = Tienda Virtual de Tenis = = = = = =")
        print("1. Admin")
        print("2. Cliente")
        print("3. Salir")
        opcion = input("Seleccione una opción: ")

        limpiar()
        if opcion == "1":
            login_admin()
        elif opcion == "2":
            login_cliente()
        elif opcion == "3":
            print("Saliendo. . . 👋")
            break
        else:
            print("Opción no válida. . . ⚠️ ")
            input("Presione ENTER para continuar...")
            limpiar()

# ---------------------- ADMIN ----------------------
def login_admin():
    user = input("Usuario admin: ")
    pwd = getpass("Contraseña: ")
    admin = managers.verificar_admin(user, pwd)
    limpiar()
    if admin:
        menu_admin()
    else:
        print("Credenciales incorrectas. . . ❌")
        input("Presione ENTER para continuar...")
        limpiar()

def menu_admin():
    while True:
        print("\n\n------ Menú Admin ------")
        print("1) Añadir tenis")
        print("2) Eliminar tenis")
        print("3) Ver pedidos")
        print("4) Completar pedido")
        print("5) Volver")
        opt = input("\nElija una opcion: ")

        limpiar()

        # --- Añadir tenis ---
        if opt == "1":
            marca = input("Marca: ")
            modelo = input("Modelo: ")
            color = input("Diseño: ")
            talla = input("Talla: ")
            precio = float(input("Precio: "))
            managers.agregar_tenis(marca, modelo, color, talla, precio)
            print("\nTenis agregado. . . ✅")

        # --- Eliminar tenis ---
        elif opt == "2":
            tenis = managers.listar_tenis()
            if not tenis:
                print("No hay tenis registrados. . . ⚠️")
            else:
                print("\n{:<4} {:<8} {:<12} {:<22} {:<10}".format("ID", "Marca", "Modelo", "Color", "Precio"))
                print("-"*60)
                for t in tenis:
                    print("{:<4} {:<8} {:<12} {:<22} ${:<10.2f}".format(
                        t.id, t.marca, t.modelo, t.color, t.precio
                    ))

                tenis_id = int(input("\nID a eliminar: "))
                confirm = input("¿Seguro que deseas eliminar este tenis? (s/n): ").lower()

                if confirm == "s":
                    if managers.eliminar_tenis(tenis_id):
                        print("Tenis eliminado. . . ✅")
                    else:
                        print("Tenis no encontrado. . . ⚠️")
                else:
                    print("Operación cancelada.")

        # --- Ver pedidos ---
        elif opt == "3":
            pedidos = managers.listar_pedidos()
            if not pedidos:
                print("No hay pedidos registrados. . .")
            else:
                print("\n----- LISTA DE PEDIDOS -----\n")
                for p in pedidos:
                    print(f"ID Pedido: {p.id}")
                    print(f"Cliente : {p.cliente.nombre}")
                    print(f"Celular : {p.cliente.celular}")
                    print(f"Fecha   : {p.fecha}")
                    print(f"Estado  : {p.estado}")
                    print(f"Tenis   : {p.tenis.marca} {p.tenis.modelo}")
                    print(f"Precio  : Bs {p.precio}")
                    print("-" * 40)

        # --- Completar pedido ---
        elif opt == "4":
            pedidos = managers.listar_pedidos()
            if not pedidos:
                print("No hay pedidos para completar. . . ⚠️")
            else:
                for p in pedidos:
                    print(f"{p.id} - {p.cliente.nombre} pidió {p.tenis.marca} {p.tenis.modelo}")

                pid = int(input("\nID del pedido a completar: "))

                pedido = Pedido.get_or_none(Pedido.id == pid)
                if pedido:
                    confirm = input("¿Confirmar completar pedido? (s/n): ").lower()
                    if confirm == "s":
                        pedido.estado = "Completado"
                        pedido.save()
                        print("\nPedido marcado como COMPLETADO. . . ✅")
                    else:
                        print("Operación cancelada.")
                else:
                    print("\nPedido no encontrado. . . ❌")

        elif opt == "5":
            limpiar()
            break

        else:
            print("Opción no válida. . . ⚠️")

        input("\nPresione ENTER para continuar...")
        limpiar()

# ---------------------- CLIENTE ----------------------
def login_cliente():
    nombre = input("Ingrese su nombre de usuario: ")
    cliente = managers.obtener_o_crear_cliente(nombre)
    limpiar()
    menu_cliente(cliente)

def menu_cliente(cliente):
    while True:
        print(f"\n------ Menú Cliente ({cliente.nombre}) ------")
        print("1) Ver tenis")
        print("2) Hacer pedido")
        print("3) Mis pedidos")     # NUEVO
        print("4) Volver")
        opt = input("Elija una opcion: ")

        limpiar()

        # --- Ver tenis ---
        if opt == "1":
            tenis = managers.listar_tenis()
            if not tenis:
                print("No hay tenis disponibles. . . ⚠️ ")
            else:
                print("\n{:<4} {:<8} {:<12} {:<22} {:<10}".format("ID", "Marca", "Modelo", "Color", "Precio"))
                print("-"*60)
                for t in tenis:
                    print("{:<4} {:<8} {:<12} {:<22} Bs{:<10.2f}".format(
                        t.id, t.marca, t.modelo, t.color, t.precio
                    ))

        # --- Hacer pedido ---
        elif opt == "2":
            tenis = managers.listar_tenis()
            if not tenis:
                print("No hay tenis para pedir. . . ⚠️ ")
                continue

            for t in tenis:
                print("{:<4} {:<8} {:<12} {:<22}".format(t.id, t.marca, t.modelo, t.color))

            tid = int(input("ID del tenis a pedir: "))
            celular = input("Ingrese su número de celular: ")

            ok, msg = managers.hacer_pedido(cliente, tid, celular)
            print(msg)

        # --- Mis pedidos (NUEVO) ---
        elif opt == "3":
            pedidos = cliente.pedidos
            if not pedidos:
                print("No tienes pedidos aún. . .")
            else:
                for p in pedidos:
                    print("-" * 40)
                    print(f"ID Pedido : {p.id}")
                    print(f"Fecha     : {p.fecha}")
                    print(f"Tenis     : {p.tenis.marca} {p.tenis.modelo}")
                    print(f"Precio    : Bs {p.precio}")
                    print(f"Estado    : {p.estado}")

        elif opt == "4":
            limpiar()
            break
        else:
            print("Opción no válida. . . ⚠️")

        input("\nPresione ENTER para continuar...")
        limpiar()


# ---------------------- MAIN ----------------------
if __name__ == "__main__":
    # Crear admin por defecto (cris/14253) si no existe
    if not managers.verificar_admin("cris", "14253"):
        managers.crear_admin("cris", "14253")
    menu_principal()
