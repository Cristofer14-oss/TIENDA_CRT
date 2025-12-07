import tkinter as tk
from tkinter import ttk, messagebox
from core import managers
import datetime

# ========================= ESTILOS GLOBALES =========================
def configurar_estilos():
    style = ttk.Style()
    style.theme_use("clam")

    style.configure(
        "Custom.Treeview",
        background="#f5f5f5",
        foreground="#000000",
        rowheight=28,
        fieldbackground="#ffffff",
        font=("Arial", 11)
    )
    style.configure(
        "Custom.Treeview.Heading",
        background="#4CAF50",
        foreground="white",
        font=("Arial", 11, "bold")
    )
    style.map(
        "Custom.Treeview",
        background=[("selected", "#91d18b")]
    )

    style.configure(
        "TButton",
        font=("Arial", 12),
        background="#2196F3",
        foreground="white",
        padding=6
    )
    style.map("TButton", background=[("active", "#0b7dda")])

# ====================================================================

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Tienda Virtual de Tenis")
        self.root.geometry("700x520")
        self.root.configure(bg="#e8f0fe") 

        configurar_estilos()

        self.frame_actual = None
        self.menu_principal()

    def cambiar_frame(self, nuevo_frame):
        if self.frame_actual:
            self.frame_actual.destroy()
        self.frame_actual = nuevo_frame
        self.frame_actual.pack(fill="both", expand=True)

    # ===================== MENÚ PRINCIPAL =====================
    def menu_principal(self):
        frame = tk.Frame(self.root, bg="#e8f0fe")

        tk.Label(
            frame, text="Tienda Virtual de Tenis",
            font=("Arial", 22, "bold"),
            bg="#e8f0fe", fg="#1a237e"
        ).pack(pady=30)

        ttk.Button(frame, text="Ingresar como Admin", width=30, command=self.login_admin).pack(pady=10)
        ttk.Button(frame, text="Ingresar como Cliente", width=30, command=self.login_cliente).pack(pady=10)
        ttk.Button(frame, text="Salir", width=30, command=self.root.quit).pack(pady=10)

        self.cambiar_frame(frame)

    # ========================= ADMIN =========================
    def login_admin(self):
        frame = tk.Frame(self.root, bg="#f0f8ff")

        tk.Label(frame, text="Login Admin", font=("Arial", 18, "bold"),
                 bg="#f0f8ff", fg="#0d47a1").pack(pady=20)

        tk.Label(frame, text="Usuario", bg="#f0f8ff").pack()
        user_entry = tk.Entry(frame, font=("Arial", 12))
        user_entry.pack()

        tk.Label(frame, text="Contraseña", bg="#f0f8ff").pack()

        pwd_entry = tk.Entry(frame, show="*", font=("Arial", 12))
        pwd_entry.pack()

        # ⚠ Evitar pegar o mostrar caracteres especiales
        pwd_entry.bind("<Control-v>", lambda e: "break")
        pwd_entry.bind("<Button-3>", lambda e: "break")

        def verificar():
            user, pwd = user_entry.get(), pwd_entry.get()

            if managers.verificar_admin(user, pwd):
                self.menu_admin()
            else:
                messagebox.showerror("Error", "Credenciales incorrectas")

        ttk.Button(frame, text="Ingresar", command=verificar).pack(pady=10)
        ttk.Button(frame, text="Volver", command=self.menu_principal).pack(pady=5)

        self.cambiar_frame(frame)

    def menu_admin(self):
        frame = tk.Frame(self.root, bg="#e8f5e9")

        tk.Label(
            frame, text="Menú Admin",
            font=("Arial", 18, "bold"),
            bg="#e8f5e9", fg="#1b5e20"
        ).pack(pady=20)

        ttk.Button(frame, text="Añadir tenis", width=30, command=self.admin_agregar).pack(pady=10)
        ttk.Button(frame, text="Eliminar tenis", width=30, command=self.admin_eliminar).pack(pady=10)
        ttk.Button(frame, text="Ver pedidos", width=30, command=self.admin_pedidos).pack(pady=10)
        ttk.Button(frame, text="Completar Pedido", width=30, command=self.admin_completar_pedido).pack(pady=10)
        ttk.Button(frame, text="Volver", width=30, command=self.menu_principal).pack(pady=10)

        self.cambiar_frame(frame)


    # ---------------- AGREGAR TENIS ----------------
    def admin_agregar(self):
        frame = tk.Frame(self.root, bg="#fff8e1")

        tk.Label(frame, text="Agregar Tenis",
                 font=("Arial", 18, "bold"),
                 bg="#fff8e1", fg="#e65100").pack(pady=20)

        entradas = {}
        for campo in ["Marca", "Modelo", "Color", "Talla", "Precio"]:
            tk.Label(frame, text=campo, font=("Arial", 12), bg="#fff8e1").pack()
            e = tk.Entry(frame, font=("Arial", 12))
            e.pack(pady=3)
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

        ttk.Button(frame, text="Guardar", command=guardar).pack(pady=10)
        ttk.Button(frame, text="Volver", command=self.menu_admin).pack(pady=10)

        self.cambiar_frame(frame)

    # ---------------- ELIMINAR TENIS ----------------
    def admin_eliminar(self):
        frame = tk.Frame(self.root, bg="#fbe9e7")

        tk.Label(frame, text="Eliminar Tenis", font=("Arial", 18, "bold"),
                 bg="#fbe9e7", fg="#bf360c").pack(pady=20)

        cols = ("ID", "Marca", "Modelo", "Color", "Precio")
        tabla = ttk.Treeview(frame, columns=cols, show="headings", style="Custom.Treeview")
        for c in cols:
            tabla.heading(c, text=c)
        tabla.pack(fill="both", expand=True, pady=10)

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

        ttk.Button(frame, text="Eliminar seleccionado", command=eliminar).pack(pady=10)
        ttk.Button(frame, text="Volver", command=self.menu_admin).pack(pady=10)

        self.cambiar_frame(frame)

    # ---------------- VER PEDIDOS ----------------
    def admin_pedidos(self):
        frame = tk.Frame(self.root, bg="#ede7f6")

        tk.Label(frame, text="Pedidos", font=("Arial", 18, "bold"),
                 bg="#ede7f6", fg="#4a148c").pack(pady=20)

        cols = ("ID", "Cliente", "Celular", "Tenis", "Precio", "Fecha", "Estado")
        tabla = ttk.Treeview(frame, columns=cols, show="headings", style="Custom.Treeview")
        for c in cols:
            tabla.heading(c, text=c)
        tabla.pack(fill="both", expand=True, pady=10)

        for p in managers.listar_pedidos():
            tabla.insert(
                "", "end",
                values=(
                    p.id,
                    p.cliente.nombre,
                    p.cliente.celular,
                    f"{p.tenis.marca} {p.tenis.modelo}",
                    p.precio,
                    p.fecha,
                    p.estado
                )
            )

        ttk.Button(frame, text="Volver", command=self.menu_admin).pack(pady=10)

        self.cambiar_frame(frame)


    # -------- COMPLETAR PEDIDO (ELIMINAR) --------
    def admin_completar_pedido(self):
        frame = tk.Frame(self.root, bg="#e0f7fa")

        tk.Label(frame, text="Completar Pedido",
                 font=("Arial", 18, "bold"),
                 bg="#e0f7fa", fg="#006064").pack(pady=20)

        cols = ("ID", "Cliente", "Tenis")
        tabla = ttk.Treeview(frame, columns=cols, show="headings", style="Custom.Treeview")
        for c in cols:
            tabla.heading(c, text=c)
        tabla.pack(fill="both", expand=True, pady=10)

        for p in managers.listar_pedidos():
            tabla.insert("", "end", values=(p.id, p.cliente.nombre, f"{p.tenis.marca} {p.tenis.modelo}"))

        def completar():
            seleccionado = tabla.selection()
            if not seleccionado:
                return messagebox.showwarning("Aviso", "Seleccione un pedido")

            pid = tabla.item(seleccionado[0])["values"][0]

            if managers.eliminar_pedido(pid):
                messagebox.showinfo("Éxito", "Pedido completado ✔")
                self.admin_completar_pedido()
            else:
                messagebox.showerror("Error", "No se encontró el pedido")

        ttk.Button(frame, text="Completar Pedido", command=completar).pack(pady=10)
        ttk.Button(frame, text="Volver", command=self.menu_admin).pack(pady=10)

        self.cambiar_frame(frame)

    # ========================= CLIENTE =========================
    def login_cliente(self):
        frame = tk.Frame(self.root, bg="#e3f2fd")

        tk.Label(frame, text="Ingresar como Cliente",
                 font=("Arial", 18, "bold"),
                 bg="#e3f2fd", fg="#0d47a1").pack(pady=20)

        tk.Label(frame, text="Nombre", bg="#e3f2fd").pack()
        nombre_entry = tk.Entry(frame, font=("Arial", 12))
        nombre_entry.pack()

        def entrar():
            nombre = nombre_entry.get()
            self.cliente = managers.obtener_o_crear_cliente(nombre)
            self.menu_cliente()

        ttk.Button(frame, text="Entrar", command=entrar).pack(pady=10)
        ttk.Button(frame, text="Volver", command=self.menu_principal).pack(pady=5)

        self.cambiar_frame(frame)

    def menu_cliente(self):
        frame = tk.Frame(self.root, bg="#e8f5e9")
    
        tk.Label(frame, text=f"Menú Cliente ({self.cliente.nombre})",
                 font=("Arial", 18, "bold"),
                 bg="#e8f5e9", fg="#1b5e20").pack(pady=20)
    
        ttk.Button(frame, text="Ver Tenis", width=30, command=self.cliente_ver_tenis).pack(pady=10)
        ttk.Button(frame, text="Hacer Pedido", width=30, command=self.cliente_hacer_pedido).pack(pady=10)
        ttk.Button(frame, text="Mis Pedidos", width=30, command=self.cliente_ver_pedidos).pack(pady=10)  # ← NUEVO
        ttk.Button(frame, text="Volver", width=30, command=self.menu_principal).pack(pady=10)
    
        self.cambiar_frame(frame)
    
    # ---------------- VER TENIS ----------------
    def cliente_ver_tenis(self):
        frame = tk.Frame(self.root, bg="#fffde7")

        tk.Label(frame, text="Tenis Disponibles",
                 font=("Arial", 18, "bold"),
                 bg="#fffde7", fg="#f57f17").pack(pady=20)

        cols = ("ID", "Marca", "Modelo", "Color", "Precio")
        tabla = ttk.Treeview(frame, columns=cols, show="headings", style="Custom.Treeview")
        for c in cols:
            tabla.heading(c, text=c)
        tabla.pack(fill="both", expand=True, pady=10)

        for t in managers.listar_tenis():
            tabla.insert("", "end", values=(t.id, t.marca, t.modelo, t.color, t.precio))

        ttk.Button(frame, text="Volver", command=self.menu_cliente).pack(pady=10)

        self.cambiar_frame(frame)

    # ---------------- HACER PEDIDO ----------------
    def cliente_hacer_pedido(self):
        frame = tk.Frame(self.root, bg="#f3e5f5")

        tk.Label(frame, text="Seleccionar Tenis",
                 font=("Arial", 18, "bold"),
                 bg="#f3e5f5", fg="#6a1b9a").pack(pady=20)

        cols = ("ID", "Marca", "Modelo", "Color", "Precio")
        tabla = ttk.Treeview(frame, columns=cols, show="headings", style="Custom.Treeview")
        for c in cols:
            tabla.heading(c, text=c)
        tabla.pack(fill="both", expand=True, pady=10)

        for t in managers.listar_tenis():
            tabla.insert("", "end", values=(t.id, t.marca, t.modelo, t.color, t.precio))

        def pedir():
            seleccionado = tabla.selection()
            if not seleccionado:
                return messagebox.showwarning("Aviso", "Seleccione un tenis")

            tid = tabla.item(seleccionado[0])["values"][0]

            # FECHA SIN HORA
            fecha = datetime.date.today().strftime("%Y-%m-%d")

            ok, msg = managers.hacer_pedido(self.cliente, tid, fecha)
            messagebox.showinfo("Resultado", msg)

        ttk.Button(frame, text="Hacer pedido", command=pedir).pack(pady=10)
        ttk.Button(frame, text="Volver", command=self.menu_cliente).pack(pady=10)

        self.cambiar_frame(frame)
    # ---------------- VER PEDIDOS ----------------
    def cliente_ver_pedidos(self):
        frame = tk.Frame(self.root, bg="#e0f2f1")
    
        tk.Label(frame, text="Mis Pedidos",
                 font=("Arial", 18, "bold"),
                 bg="#e0f2f1", fg="#004d40").pack(pady=20)
    
        cols = ("ID", "Tenis", "Precio", "Fecha", "Estado")
        tabla = ttk.Treeview(frame, columns=cols, show="headings", style="Custom.Treeview")
        for c in cols:
            tabla.heading(c, text=c)
        tabla.pack(fill="both", expand=True, pady=10)
    
        pedidos = self.cliente.pedidos  # Solo los del cliente actual
        for p in pedidos:
            tabla.insert(
                "", "end",
                values=(
                    p.id,
                    f"{p.tenis.marca} {p.tenis.modelo}",
                    p.precio,
                    p.fecha,
                    p.estado
                )
            )
    
        ttk.Button(frame, text="Volver", command=self.menu_cliente).pack(pady=10)
    
        self.cambiar_frame(frame)
    


# ========================= MAIN =========================
if __name__ == "__main__":
    if not managers.verificar_admin("cris", "14253"):
        managers.crear_admin("cris", "14253")

    root = tk.Tk()
    App(root)
    root.mainloop()
