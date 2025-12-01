import tkinter as tk
from tkinter import ttk, messagebox
from core import managers

# ========================= VENTANA PRINCIPAL =========================
class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Tienda Virtual de Tenis")
        self.root.geometry("650x500")

        self.frame_actual = None
        self.menu_principal()

    # ---------------- CAMBIAR FRAME ----------------
    def cambiar_frame(self, nuevo_frame):
        if self.frame_actual:
            self.frame_actual.destroy()
        self.frame_actual = nuevo_frame
        self.frame_actual.pack(fill="both", expand=True)

    # ===================== MENÚ PRINCIPAL =====================
    def menu_principal(self):
        frame = tk.Frame(self.root)
        tk.Label(frame, text="Tienda Virtual de Tenis", font=("Arial", 18, "bold")).pack(pady=20)

        tk.Button(frame, text="Ingresar como Admin", width=30, command=self.login_admin).pack(pady=10)
        tk.Button(frame, text="Ingresar como Cliente", width=30, command=self.login_cliente).pack(pady=10)
        tk.Button(frame, text="Salir", width=30, command=self.root.quit).pack(pady=10)

        self.cambiar_frame(frame)

    # ========================= ADMIN =========================
    def login_admin(self):
        frame = tk.Frame(self.root)
        tk.Label(frame, text="Login Admin", font=("Arial", 16)).pack(pady=20)

        tk.Label(frame, text="Usuario").pack()
        user_entry = tk.Entry(frame)
        user_entry.pack()

        tk.Label(frame, text="Contraseña").pack()
        pwd_entry = tk.Entry(frame, show="*")
        pwd_entry.pack()

        def verificar():
            user = user_entry.get()
            pwd = pwd_entry.get()

            if managers.verificar_admin(user, pwd):
                self.menu_admin()
            else:
                messagebox.showerror("Error", "Credenciales incorrectas")

        tk.Button(frame, text="Ingresar", command=verificar).pack(pady=10)
        tk.Button(frame, text="Volver", command=self.menu_principal).pack(pady=5)

        self.cambiar_frame(frame)

    def menu_admin(self):
        frame = tk.Frame(self.root)
        tk.Label(frame, text="Menú Admin", font=("Arial", 16)).pack(pady=20)

        tk.Button(frame, text="Añadir tenis", width=30, command=self.admin_agregar).pack(pady=10)
        tk.Button(frame, text="Eliminar tenis", width=30, command=self.admin_eliminar).pack(pady=10)
        tk.Button(frame, text="Ver pedidos", width=30, command=self.admin_pedidos).pack(pady=10)
        tk.Button(frame, text="Volver", width=30, command=self.menu_principal).pack(pady=10)

        self.cambiar_frame(frame)

    # ---------------- AGREGAR TENIS ----------------
    def admin_agregar(self):
        frame = tk.Frame(self.root)
        tk.Label(frame, text="Agregar Tenis", font=("Arial", 16)).pack(pady=20)

        entradas = {}
        for campo in ["Marca", "Modelo", "Color", "Talla", "Precio"]:
            tk.Label(frame, text=campo).pack()
            e = tk.Entry(frame)
            e.pack()
            entradas[campo] = e

        def guardar():
            try:
                managers.agregar_tenis(
                    entradas["Marca"].get(),
                    entradas["Modelo"].get(),
                    entradas["Color"].get(),
                    entradas["Talla"].get(),
                    float(entradas["Precio"].get())
                )
                messagebox.showinfo("Éxito", "Tenis agregado")
                self.menu_admin()
            except:
                messagebox.showerror("Error", "Revise los datos")

        tk.Button(frame, text="Guardar", command=guardar).pack(pady=10)
        tk.Button(frame, text="Volver", command=self.menu_admin).pack(pady=10)

        self.cambiar_frame(frame)

    # ---------------- ELIMINAR TENIS ----------------
    def admin_eliminar(self):
        frame = tk.Frame(self.root)
        tk.Label(frame, text="Eliminar Tenis", font=("Arial", 16)).pack(pady=20)

        cols = ("ID", "Marca", "Modelo", "Color", "Precio")
        tabla = ttk.Treeview(frame, columns=cols, show="headings")
        for c in cols:
            tabla.heading(c, text=c)
        tabla.pack(fill="both", expand=True)

        for t in managers.listar_tenis():
            tabla.insert("", "end", values=(t.id, t.marca, t.modelo, t.color, t.precio))

        def eliminar():
            seleccionado = tabla.selection()
            if not seleccionado:
                return messagebox.showwarning("Aviso", "Seleccione un tenis")

            tenis_id = tabla.item(seleccionado[0])["values"][0]

            if managers.eliminar_tenis(tenis_id):
                messagebox.showinfo("Éxito", "Tenis eliminado")
                self.admin_eliminar()
            else:
                messagebox.showerror("Error", "No se encontró el tenis")

        tk.Button(frame, text="Eliminar seleccionado", command=eliminar).pack(pady=10)
        tk.Button(frame, text="Volver", command=self.menu_admin).pack(pady=10)

        self.cambiar_frame(frame)

    # ---------------- VER PEDIDOS ----------------
    def admin_pedidos(self):
        frame = tk.Frame(self.root)
        tk.Label(frame, text="Pedidos", font=("Arial", 16)).pack(pady=20)

        cols = ("Cliente", "Marca", "Modelo")
        tabla = ttk.Treeview(frame, columns=cols, show="headings")
        for c in cols:
            tabla.heading(c, text=c)
        tabla.pack(fill="both", expand=True)

        for p in managers.listar_pedidos():
            tabla.insert("", "end", values=(p.cliente.nombre, p.tenis.marca, p.tenis.modelo))

        tk.Button(frame, text="Volver", command=self.menu_admin).pack(pady=10)

        self.cambiar_frame(frame)

    # ========================= CLIENTE =========================
    def login_cliente(self):
        frame = tk.Frame(self.root)
        tk.Label(frame, text="Ingresar como Cliente", font=("Arial", 16)).pack(pady=20)

        tk.Label(frame, text="Nombre").pack()
        nombre_entry = tk.Entry(frame)
        nombre_entry.pack()

        def entrar():
            nombre = nombre_entry.get()
            self.cliente = managers.obtener_o_crear_cliente(nombre)
            self.menu_cliente()

        tk.Button(frame, text="Entrar", command=entrar).pack(pady=10)
        tk.Button(frame, text="Volver", command=self.menu_principal).pack(pady=5)

        self.cambiar_frame(frame)

    def menu_cliente(self):
        frame = tk.Frame(self.root)
        tk.Label(frame, text=f"Menú Cliente ({self.cliente.nombre})", font=("Arial", 16)).pack(pady=20)

        tk.Button(frame, text="Ver Tenis", width=30, command=self.cliente_ver_tenis).pack(pady=10)
        tk.Button(frame, text="Hacer Pedido", width=30, command=self.cliente_hacer_pedido).pack(pady=10)
        tk.Button(frame, text="Volver", width=30, command=self.menu_principal).pack(pady=10)

        self.cambiar_frame(frame)

    # ---------------- VER TENIS (TABLA) ----------------
    def cliente_ver_tenis(self):
        frame = tk.Frame(self.root)
        tk.Label(frame, text="Tenis Disponibles", font=("Arial", 16)).pack(pady=20)

        cols = ("ID", "Marca", "Modelo", "Color", "Precio")
        tabla = ttk.Treeview(frame, columns=cols, show="headings")
        for c in cols:
            tabla.heading(c, text=c)
        tabla.pack(fill="both", expand=True)

        for t in managers.listar_tenis():
            tabla.insert("", "end", values=(t.id, t.marca, t.modelo, t.color, t.precio))

        tk.Button(frame, text="Volver", command=self.menu_cliente).pack(pady=10)

        self.cambiar_frame(frame)

    # ---------------- HACER PEDIDO (TABLA) ----------------
    def cliente_hacer_pedido(self):
        frame = tk.Frame(self.root)
        tk.Label(frame, text="Seleccionar Tenis", font=("Arial", 16)).pack(pady=20)

        cols = ("ID", "Marca", "Modelo", "Color", "Precio")
        tabla = ttk.Treeview(frame, columns=cols, show="headings")
        for c in cols:
            tabla.heading(c, text=c)
        tabla.pack(fill="both", expand=True)

        for t in managers.listar_tenis():
            tabla.insert("", "end", values=(t.id, t.marca, t.modelo, t.color, t.precio))

        def pedir():
            seleccionado = tabla.selection()
            if not seleccionado:
                return messagebox.showwarning("Aviso", "Seleccione un tenis")

            tid = tabla.item(seleccionado[0])["values"][0]

            ok, msg = managers.hacer_pedido(self.cliente, tid)
            messagebox.showinfo("Resultado", msg)

        tk.Button(frame, text="Hacer pedido", command=pedir).pack(pady=10)
        tk.Button(frame, text="Volver", command=self.menu_cliente).pack(pady=10)

        self.cambiar_frame(frame)


# ========================= MAIN =========================
if __name__ == "__main__":
    # Crear admin por defecto
    if not managers.verificar_admin("cris", "14253"):
        managers.crear_admin("cris", "14253")

    root = tk.Tk()
    App(root)
    root.mainloop()

