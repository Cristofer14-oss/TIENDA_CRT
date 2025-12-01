import os
from core import managers

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
    pwd = input("Contraseña: ")
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
        print("4) Volver")
        opt = input("\nElija una opcion: ")

        limpiar()
        if opt == "1":
            marca = input("Marca: ")
            modelo = input("Modelo: ")
            color = input("Diseño: ")
            talla = input("Talla: ")
            precio = float(input("Precio: "))
            managers.agregar_tenis(marca, modelo, color, talla, precio)
            print("\nTenis agregado. . . ✅")

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
                if managers.eliminar_tenis(tenis_id):
                    print("Tenis eliminado. . . ✅")
                else:
                    print("Tenis no encontrado. . . ⚠️")

        elif opt == "3":
            pedidos = managers.listar_pedidos()
            if not pedidos:
                print("No hay pedidos registrados. . .")
            else:
                for p in pedidos:
                    print(f"Cliente: {p.cliente.nombre} pidió {p.tenis.marca} {p.tenis.modelo}")

        elif opt == "4":
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
        print("3) Volver")
        opt = input("Elija una opcion: ")

        limpiar()
        if opt == "1":
            tenis = managers.listar_tenis()
            if not tenis:
                print("No hay tenis disponibles. . . ⚠️ ")
            else:
                print("\n{:<4} {:<8} {:<12} {:<22} {:<10}".format("ID", "Marca", "Modelo", "Color", "Precio"))
                print("-"*60)
                for t in tenis:
                    print("{:<4} {:<8} {:<12} {:<22} Bs {:<10.2f}".format(
                        t.id, t.marca, t.modelo, t.color, t.precio
                    ))

        elif opt == "2":
            tenis = managers.listar_tenis()
            if not tenis:
                print("No hay tenis para pedir. . . ⚠️ ")
                continue
            for t in tenis:
                print(f"{t.id} - {t.marca} {t.modelo}")
            tid = int(input("ID del tenis a pedir: "))
            ok, msg = managers.hacer_pedido(cliente, tid)
            print(msg)

        elif opt == "3":
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
