import curses
from core import managers

# ------------------- TITULO PERMANENTE -------------------
def draw_title(stdscr):
    stdscr.clear()
    h, w = stdscr.getmaxyx()

    title = " TIENDA DE TENIS CRT "
    box_width = len(title) + 6
    start_x = (w // 2) - (box_width // 2)

    # Activar color azul
    curses.init_pair(1, curses.COLOR_CYAN, curses.COLOR_BLACK)
    color = curses.color_pair(1) | curses.A_BOLD

    # Bordes
    stdscr.attron(color)
    stdscr.addstr(0, start_x, "╔" + "═" * (box_width - 2) + "╗")
    stdscr.addstr(1, start_x, "║" + title.center(box_width - 2) + "║")
    stdscr.addstr(2, start_x, "╚" + "═" * (box_width - 2) + "╝")
    stdscr.attroff(color)

# ------------------- MENÚ CLIENTE -------------------
def menu_cliente(stdscr, cliente):
    options = ["1. Ver tenis", "2. Hacer pedido", "3. Volver"]
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

        if key == curses.KEY_UP:
            selected = (selected - 1) % len(options)
        elif key == curses.KEY_DOWN:
            selected = (selected + 1) % len(options)
        elif key == curses.KEY_ENTER or key in [10, 13]:

            # ---------- VER TENIS ----------
            if selected == 0:
                tenis = managers.listar_tenis()
                stdscr.clear()
                draw_title(stdscr)

                if not tenis:
                    stdscr.addstr(3, 2, "No hay tenis disponibles ⚠️")
                else:
                    stdscr.addstr(3, 2,
                        f"{'ID':<4} {'Marca':<12} {'Modelo':<15} {'Color':<20} {'Talla':<6} {'Precio (Bs)':<12}"
                    )
                    stdscr.addstr(4, 2, "-" * 70)

                    y = 5
                    for t in tenis:
                        stdscr.addstr(
                            y,
                            2,
                            f"{t.id:<4} {t.marca:<12} {t.modelo:<15} {t.color:<20} {t.talla:<6} {t.precio:<12.2f}"
                        )
                        y += 1

                stdscr.getch()

            # ---------- HACER PEDIDO ----------
            elif selected == 1:
                tenis = managers.listar_tenis()
                stdscr.clear()
                draw_title(stdscr)

                if not tenis:
                    stdscr.addstr(3, 2, "No hay tenis disponibles para pedir ⚠️")
                    stdscr.getch()
                else:
                    stdscr.addstr(3, 2, "Ingrese el ID del tenis a pedir:\n")

                    y = 4
                    for t in tenis:
                        stdscr.addstr(
                            y,
                            3,
                            f"{t.id:<4} {t.marca:<12} {t.modelo:<15} {t.color:<12} "
                            f"{t.talla:<6} {t.precio:<12.2f}"
                        )
                        y += 1

                    curses.echo()
                    tid = int(stdscr.getstr(y + 1, 2).decode())
                    curses.noecho()

                    ok, msg = managers.hacer_pedido(cliente, tid)
                    stdscr.addstr(y + 3, 2, msg)
                    stdscr.getch()

            # ---------- VOLVER ----------
            elif selected == 2:
                break

# ------------------- MENÚ ADMIN -------------------
def menu_admin(stdscr):
    options = ["1. Añadir tenis", "2. Eliminar tenis", "3. Ver pedidos", "4. Volver"]
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

        if key == curses.KEY_UP:
            selected = (selected - 1) % len(options)
        elif key == curses.KEY_DOWN:
            selected = (selected + 1) % len(options)
        elif key in [10, 13]:

            # AÑADIR
            if selected == 0:
                stdscr.clear()
                draw_title(stdscr)
                stdscr.addstr(3, 2, "Añadir tenis:\n")
                
                curses.echo()
                marca = input_field(stdscr, 4, "Marca: ")
                modelo = input_field(stdscr, 5, "Modelo: ")
                color = input_field(stdscr, 6, "Color: ")
                talla = input_field(stdscr, 7, "Talla: ")
                precio = float(input_field(stdscr, 8, "Precio: "))
                curses.noecho()

                managers.agregar_tenis(marca, modelo, color, talla, precio)
                stdscr.addstr(10, 2, "Tenis agregado correctamente ✔")
                stdscr.getch()

            # ELIMINAR
            elif selected == 1:
                tenis = managers.listar_tenis()
                stdscr.clear()
                draw_title(stdscr)

                if not tenis:
                    stdscr.addstr(3, 2, "No hay tenis registrados ⚠️")
                    stdscr.getch()
                else:
                    stdscr.addstr(3, 2, "ID | Marca | Modelo | Color | Talla | Precio (Bs)")
                    stdscr.addstr(4, 2, "-" * 70)

                    y = 4
                    for t in tenis:
                        stdscr.addstr(
                            y,
                            3,
                            f"{t.id:<4} {t.marca:<12} {t.modelo:<15} {t.color:<20} "
                            f"{t.talla:<6} {t.precio:<12.2f}"
                        )
                        y += 1

                    curses.echo()
                    tenis_id = int(input_field(stdscr, y + 2, "ID a eliminar: "))
                    curses.noecho()

                    if managers.eliminar_tenis(tenis_id):
                        stdscr.addstr(y + 4, 2, "Tenis eliminado ✔")
                    else:
                        stdscr.addstr(y + 4, 2, "Tenis no encontrado ⚠️")
                    stdscr.getch()

            # VER PEDIDOS
            elif selected == 2:
                pedidos = managers.listar_pedidos()
                stdscr.clear()
                draw_title(stdscr)

                if not pedidos:
                    stdscr.addstr(3, 2, "No hay pedidos registrados ⚠️")
                else:
                    y = 3
                    for p in pedidos:
                        stdscr.addstr(
                            y,
                            3,
                            f"Cliente: {p.cliente.nombre} pidió {p.tenis.marca} {p.tenis.modelo}"
                        )
                        y += 1

                stdscr.getch()

            # VOLVER
            elif selected == 3:
                break

# ------------------- INPUT FIELD -------------------
def input_field(stdscr, row, label):
    stdscr.addstr(row, 2, label)
    return stdscr.getstr(row, len(label) + 3).decode()

# ------------------- LOGIN -------------------
def login_cliente(stdscr):
    stdscr.clear()
    draw_title(stdscr)

    curses.echo()
    stdscr.addstr(3, 2, "Ingrese su nombre de usuario: ")
    nombre = stdscr.getstr(4, 2).decode()
    curses.noecho()

    cliente = managers.obtener_o_crear_cliente(nombre)
    menu_cliente(stdscr, cliente)

def login_admin(stdscr):
    stdscr.clear()
    draw_title(stdscr)

    curses.echo()
    stdscr.addstr(3, 2, "Usuario admin: ")
    user = stdscr.getstr(4, 2).decode()

    stdscr.addstr(6, 2, "Contraseña: ")
    pwd = stdscr.getstr(7, 2).decode()
    curses.noecho()

    admin = managers.verificar_admin(user, pwd)
    if admin:
        menu_admin(stdscr)
    else:
        stdscr.addstr(9, 2, "Credenciales incorrectas ❌")
        stdscr.getch()

# ------------------- MENÚ PRINCIPAL -------------------
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

        for idx, opt in enumerate(options):
            if idx == selected:
                stdscr.attron(curses.A_REVERSE)
            stdscr.addstr(4 + idx, 4, opt)
            stdscr.attroff(curses.A_REVERSE)

        key = stdscr.getch()

        if key == curses.KEY_UP:
            selected = (selected - 1) % len(options)
        elif key == curses.KEY_DOWN:
            selected = (selected + 1) % len(options)
        elif key in [10, 13]:

            if selected == 0:
                login_admin(stdscr)
            elif selected == 1:
                login_cliente(stdscr)
            elif selected == 2:
                break
if __name__ == "__main__": curses.wrapper(main)
