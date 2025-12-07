import curses
from core import managers
from datetime import datetime
from core.models import Pedido

# -----------------------------------------------------
# TITULO
# -----------------------------------------------------
def draw_title(stdscr):
    stdscr.clear()
    h, w = stdscr.getmaxyx()

    title = " TIENDA DE TENIS CRT "
    box_width = len(title) + 6
    start_x = (w // 2) - (box_width // 2)

    curses.init_pair(1, curses.COLOR_CYAN, curses.COLOR_BLACK)
    color = curses.color_pair(1) | curses.A_BOLD

    stdscr.attron(color)
    stdscr.addstr(0, start_x, "╔" + "═" * (box_width - 2) + "╗")
    stdscr.addstr(1, start_x, "║" + title.center(box_width - 2) + "║")
    stdscr.addstr(2, start_x, "╚" + "═" * (box_width - 2) + "╝")
    stdscr.attroff(color)

# -----------------------------------------------------
# INPUT FIELD
# -----------------------------------------------------
def input_field(stdscr, row, label):
    stdscr.addstr(row, 2, label)
    return stdscr.getstr(row, len(label) + 3).decode()

# -----------------------------------------------------
# FUNCION AUXILIAR: IMPRIMIR LISTA DE TENIS COMO TABLA
# -----------------------------------------------------
def mostrar_lista_tenis(stdscr, tenis, start_y=3):
    """
    Imprime una lista de tenis en formato tabla tipo Excel.
    :param stdscr: objeto curses
    :param tenis: lista de objetos tenis
    :param start_y: fila inicial para imprimir
    """
    if not tenis:
        stdscr.addstr(start_y, 2, "No hay tenis disponibles ⚠️")
        return start_y + 1

    # Definir encabezado y ancho de columnas
    headers = ["ID", "Marca", "Modelo", "Color", "Talla", "Precio Bs"]
    col_widths = [4, 12, 15, 20, 6, 10]

    y = start_y
    # Imprimir encabezado
    header_line = ""
    for h, w in zip(headers, col_widths):
        header_line += f"{h:<{w}} "
    stdscr.addstr(y, 2, header_line, curses.A_BOLD | curses.A_UNDERLINE)
    y += 1

    # Imprimir tenis
    for t in tenis:
        line = f"{t.id:<4} {t.marca:<12} {t.modelo:<15} {t.color:<20} {t.talla:<6} Bs{t.precio:<10.2f}"
        stdscr.addstr(y, 2, line[:stdscr.getmaxyx()[1]-4])
        y += 1

    return y

def mostrar_pedidos(stdscr, pedidos, prompt_completar=False):
    """
    Muestra pedidos en tabla tipo Excel.
    Si prompt_completar=True permite seleccionar un pedido para marcar como completado.
    Retorna el ID seleccionado o None si no se selecciona.
    """
    height, width = stdscr.getmaxyx()
    max_lines = height - 6  # filas disponibles
    pedidos_por_pagina = max_lines - 3

    total = len(pedidos)
    pagina = 0

    while True:
        stdscr.clear()
        draw_title(stdscr)

        if total == 0:
            stdscr.addstr(4, 2, "No hay pedidos registrados ⚠️")
            stdscr.getch()
            return None

        inicio = pagina * pedidos_por_pagina
        fin = inicio + pedidos_por_pagina
        pagina_pedidos = pedidos[inicio:fin]

        # Encabezado
        headers = ["ID", "Cliente", "Celular", "Fecha", "Estado", "Marca", "Modelo"]
        col_widths = [4, 15, 12, 12, 10, 12, 15]  # se pueden ajustar
        y = 3

        header_line = ""
        for h, w in zip(headers, col_widths):
            header_line += f"{h:<{w}} "
        stdscr.addstr(y, 2, header_line[:width-4], curses.A_BOLD | curses.A_UNDERLINE)
        y += 1

        # Mostrar datos
        for p in pagina_pedidos:
            line = f"{str(p.id)[:col_widths[0]-1]:<{col_widths[0]}} " \
                   f"{p.cliente.nombre[:col_widths[1]-1]:<{col_widths[1]}} " \
                   f"{p.cliente.celular[:col_widths[2]-1]:<{col_widths[2]}} " \
                   f"{str(p.fecha)[:col_widths[3]-1]:<{col_widths[3]}} " \
                   f"{p.estado[:col_widths[4]-1]:<{col_widths[4]}} " \
                   f"{p.tenis.marca[:col_widths[5]-1]:<{col_widths[5]}} " \
                   f"{p.tenis.modelo[:col_widths[6]-1]:<{col_widths[6]}}"
            stdscr.addstr(y, 2, line[:width-4])
            y += 1

        stdscr.addstr(height - 2, 2,
                      f"Página {pagina + 1} / {max(1, (total - 1) // pedidos_por_pagina + 1)}  ← Página anterior | → Página siguiente | ENTER/Q salir")

        key = stdscr.getch()
        if key in (ord('q'), ord('Q'), 10):
            break
        elif key == curses.KEY_LEFT and pagina > 0:
            pagina -= 1
        elif key == curses.KEY_RIGHT and fin < total:
            pagina += 1

    # Si es completar pedido, pedir ID
    if prompt_completar:
        curses.echo()
        stdscr.addstr(y + 1, 2, "Ingrese ID del pedido a completar: ")
        try:
            pid = int(stdscr.getstr(y + 2, 2).decode())
        except ValueError:
            pid = None
        curses.noecho()
        return pid

    return None


# -----------------------------------------------------
# CLIENTE - MENÚ
# -----------------------------------------------------
def menu_cliente(stdscr, cliente):
    options = ["1. Ver tenis", "2. Hacer pedido", "3. Mis pedidos", "4. Volver"]
    selected = 0

    while True:
        stdscr.clear()
        draw_title(stdscr)

        stdscr.addstr(3, 2, f"Cliente: {cliente.nombre}\n")

        for idx, opt in enumerate(options):
            if idx == selected:
                stdscr.attron(curses.A_REVERSE)
            stdscr.addstr(4 + idx, 4, opt)
            stdscr.attroff(curses.A_REVERSE)

        key = stdscr.getch()

        if key == curses.KEY_UP: selected = (selected - 1) % len(options)
        elif key == curses.KEY_DOWN: selected = (selected + 1) % len(options)
        elif key in [10, 13]:

            # ---------------- VER TENIS ----------------
            if selected == 0:
                tenis = managers.listar_tenis()
                stdscr.clear()
                draw_title(stdscr)
                mostrar_lista_tenis(stdscr, tenis, start_y=3)
                stdscr.getch()

            # ---------------- HACER PEDIDO ----------------
            elif selected == 1:
                tenis = managers.listar_tenis()
                stdscr.clear()
                draw_title(stdscr)
                y = mostrar_lista_tenis(stdscr, tenis, start_y=3)

                if not tenis:
                    stdscr.getch()
                else:
                    stdscr.addstr(y + 1, 2, "Seleccione ID del tenis a pedir:")
                    curses.echo()
                    tid = int(stdscr.getstr(y + 2, 2).decode())
                    celular = stdscr.getstr(y + 3, 2, 20).decode()
                    curses.noecho()

                    ok, msg = managers.hacer_pedido(cliente, tid, celular)
                    stdscr.addstr(y + 5, 2, msg)
                    stdscr.getch()

            # ---------------- MIS PEDIDOS ----------------
            elif selected == 2:
                pedidos = cliente.pedidos
                stdscr.clear()
                draw_title(stdscr)

                if not pedidos:
                    stdscr.addstr(3, 2, "No tienes pedidos aún.")
                else:
                    y = 3
                    for p in pedidos:
                        stdscr.addstr(y, 2, "-" * 60); y += 1
                        stdscr.addstr(y, 2, f"ID: {p.id}     Fecha: {p.fecha}"); y += 1
                        stdscr.addstr(y, 2, f"Tenis: {p.tenis.marca} {p.tenis.modelo}"); y += 1
                        stdscr.addstr(y, 2, f"Precio: Bs {p.precio}"); y += 1
                        stdscr.addstr(y, 2, f"Estado: {p.estado}"); y += 2

                stdscr.getch()

            # ---------------- VOLVER ----------------
            elif selected == 3:
                break

# -----------------------------------------------------
# ADMIN - MENÚ
# -----------------------------------------------------
def menu_admin(stdscr):
    options = [
        "1. Añadir tenis",
        "2. Eliminar tenis",
        "3. Ver pedidos",
        "4. Completar pedido",
        "5. Volver"
    ]
    selected = 0

    while True:
        stdscr.clear()
        draw_title(stdscr)

        stdscr.addstr(3, 2, "Menú Admin:")

        for idx, opt in enumerate(options):
            if idx == selected:
                stdscr.attron(curses.A_REVERSE)
            stdscr.addstr(4 + idx, 4, opt)
            stdscr.attroff(curses.A_REVERSE)

        key = stdscr.getch()

        if key == curses.KEY_UP: selected = (selected - 1) % len(options)
        elif key == curses.KEY_DOWN: selected = (selected + 1) % len(options)
        elif key in [10, 13]:

            # ---------------- AÑADIR ----------------
            if selected == 0:
                stdscr.clear()
                draw_title(stdscr)
                curses.echo()
                marca = input_field(stdscr, 4, "Marca: ")
                modelo = input_field(stdscr, 5, "Modelo: ")
                color = input_field(stdscr, 6, "Color: ")
                talla = input_field(stdscr, 7, "Talla: ")
                precio = float(input_field(stdscr, 8, "Precio: "))
                curses.noecho()

                managers.agregar_tenis(marca, modelo, color, talla, precio)
                stdscr.addstr(10, 2, "Tenis agregado ✔")
                stdscr.getch()

            # ---------------- ELIMINAR ----------------
            elif selected == 1:
                tenis = managers.listar_tenis()
                stdscr.clear()
                draw_title(stdscr)
                y = mostrar_lista_tenis(stdscr, tenis, start_y=3)

                if not tenis:
                    stdscr.getch()
                else:
                    curses.echo()
                    tid = int(input_field(stdscr, y + 1, "ID a eliminar: "))
                    curses.noecho()

                    if managers.eliminar_tenis(tid):
                        stdscr.addstr(y + 3, 2, "Tenis eliminado ✔")
                    else:
                        stdscr.addstr(y + 3, 2, "No encontrado ⚠️")
                    stdscr.getch()

            # ---------------- VER PEDIDOS ----------------
            elif selected == 2:
                pedidos = managers.listar_pedidos()
                mostrar_pedidos(stdscr, pedidos, prompt_completar=False)
            
            # ---------------- COMPLETAR PEDIDO ----------------
            elif selected == 3:
                pedidos = [p for p in managers.listar_pedidos() if p.estado != "Completado"]
                pid = mostrar_pedidos(stdscr, pedidos, prompt_completar=True)
                if pid is not None:
                    if managers.completar_pedido(pid):
                        stdscr.addstr(2, 2, f"Pedido {pid} marcado como completado ✔")
                    else:
                        stdscr.addstr(2, 2, "ID no encontrado ⚠️")
                    stdscr.getch()
            
            # ---------------- VOLVER ----------------
            elif selected == 4:
                break

# -----------------------------------------------------
# LOGIN CLIENTE
# -----------------------------------------------------
def login_cliente(stdscr):
    stdscr.clear()
    draw_title(stdscr)

    curses.echo()
    stdscr.addstr(3, 2, "Nombre de usuario: ")
    nombre = stdscr.getstr(4, 2).decode()
    curses.noecho()

    cliente = managers.obtener_o_crear_cliente(nombre)
    menu_cliente(stdscr, cliente)

# -----------------------------------------------------
# LOGIN ADMIN (CON CONTRASEÑA OCULTA)
# -----------------------------------------------------
def login_admin(stdscr):
    stdscr.clear()
    draw_title(stdscr)

    curses.echo()
    stdscr.addstr(3, 2, "Usuario admin: ")
    user = stdscr.getstr(4, 2).decode()
    curses.noecho()

    stdscr.addstr(6, 2, "Contraseña: ")
    curses.noecho()
    pwd = stdscr.getstr(7, 2).decode()

    admin = managers.verificar_admin(user, pwd)
    if admin:
        menu_admin(stdscr)
    else:
        stdscr.addstr(9, 2, "Credenciales incorrectas ❌")
        stdscr.getch()

# -----------------------------------------------------
# MENÚ PRINCIPAL
# -----------------------------------------------------
def main(stdscr):
    curses.curs_set(0)

    if not managers.verificar_admin("cris", "14253"):
        managers.crear_admin("cris", "14253")

    options = ["1. Admin", "2. Cliente", "3. Salir"]
    selected = 0

    while True:
        stdscr.clear()
        draw_title(stdscr)

        stdscr.addstr(3, 2, "Menú Principal:")

        for i, opt in enumerate(options):
            if i == selected:
                stdscr.attron(curses.A_REVERSE)
            stdscr.addstr(4 + i, 4, opt)
            stdscr.attroff(curses.A_REVERSE)

        key = stdscr.getch()

        if key == curses.KEY_UP: selected = (selected - 1) % len(options)
        elif key == curses.KEY_DOWN: selected = (selected + 1) % len(options)
        elif key in [10, 13]:

            if selected == 0: login_admin(stdscr)
            elif selected == 1: login_cliente(stdscr)
            elif selected == 2: break

if __name__ == "__main__":
    curses.wrapper(main)
