import tkinter as tk
from tkinter import ttk, messagebox
import time
import math

# ════════════════════════════════════════════════════════════
#  CLASE PILA
# ════════════════════════════════════════════════════════════

class Pila:
    def __init__(self):
        self.elementos = []

    def apilar(self, elemento):
        self.elementos.append(elemento)

    def desapilar(self):
        if self.esta_vacia():
            raise IndexError("Pila vacía")
        return self.elementos.pop()

    def cima(self):
        if self.esta_vacia():
            raise IndexError("Pila vacía")
        return self.elementos[-1]

    def esta_vacia(self):
        return len(self.elementos) == 0

    def tamaño(self):
        return len(self.elementos)


# ════════════════════════════════════════════════════════════
#  LÓGICA HANÓI
# ════════════════════════════════════════════════════════════

def generar_movimientos(n):
    movs = []
    def _rec(k, origen, destino, auxiliar):
        if k == 1:
            movs.append((1, origen, destino))
            return
        _rec(k - 1, origen, auxiliar, destino)
        movs.append((k, origen, destino))
        _rec(k - 1, auxiliar, destino, origen)
    _rec(n, 'A', 'C', 'B')
    return movs


# ════════════════════════════════════════════════════════════
#  LÓGICA EVALUADOR
# ════════════════════════════════════════════════════════════

def es_operador(t):
    return t in ('+', '-', '*', '/', '**')

def aplicar_op(op, a, b):
    if op == '+':  return a + b
    if op == '-':  return a - b
    if op == '*':  return a * b
    if op == '/':
        if b == 0: raise ZeroDivisionError("División por cero")
        return a / b
    if op == '**': return a ** b

def evaluar_postfija(expr):
    tokens = expr.strip().split()
    pila = Pila()
    pasos = []
    for token in tokens:
        try:
            pila.apilar(float(token))
            pasos.append(f"  PUSH {token:<8}  →  pila: {list(pila.elementos)}")
        except ValueError:
            if not es_operador(token):
                raise ValueError(f"Token inválido: '{token}'")
            if pila.tamaño() < 2:
                raise ValueError("Faltan operandos")
            b = pila.desapilar()
            a = pila.desapilar()
            r = aplicar_op(token, a, b)
            pila.apilar(r)
            pasos.append(f"  {a} {token} {b} = {r:<6}  →  pila: {list(pila.elementos)}")
    if pila.tamaño() != 1:
        raise ValueError("Expresión inválida")
    return pila.desapilar(), pasos

def evaluar_prefija(expr):
    tokens = expr.strip().split()[::-1]
    pila = Pila()
    pasos = []
    for token in tokens:
        try:
            pila.apilar(float(token))
            pasos.append(f"  PUSH {token:<8}  →  pila: {list(pila.elementos)}")
        except ValueError:
            if not es_operador(token):
                raise ValueError(f"Token inválido: '{token}'")
            if pila.tamaño() < 2:
                raise ValueError("Faltan operandos")
            a = pila.desapilar()
            b = pila.desapilar()
            r = aplicar_op(token, a, b)
            pila.apilar(r)
            pasos.append(f"  {a} {token} {b} = {r:<6}  →  pila: {list(pila.elementos)}")
    if pila.tamaño() != 1:
        raise ValueError("Expresión inválida")
    return pila.desapilar(), pasos


# ════════════════════════════════════════════════════════════
#  PALETA Y CONSTANTES
# ════════════════════════════════════════════════════════════

BG        = "#0e0e1a"
BG2       = "#16162a"
BG3       = "#1e1e38"
ACCENT    = "#7c6ff7"
ACCENT2   = "#48d6c0"
TEXT      = "#e8e8ff"
MUTED     = "#6666aa"
SUCCESS   = "#4ade80"
WARNING   = "#fbbf24"
DANGER    = "#f87171"

DISK_COLORS = [
    "#f87171", "#fb923c", "#fbbf24", "#a3e635",
    "#34d399", "#22d3ee", "#818cf8", "#c084fc",
    "#f472b6", "#94a3b8", "#60a5fa", "#e879f9",
]

FONT_TITLE  = ("Courier New", 18, "bold")
FONT_MONO   = ("Courier New", 11)
FONT_MONO_B = ("Courier New", 11, "bold")
FONT_SMALL  = ("Courier New", 9)
FONT_BIG    = ("Courier New", 28, "bold")


# ════════════════════════════════════════════════════════════
#  APLICACIÓN PRINCIPAL
# ════════════════════════════════════════════════════════════

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Estructuras de Datos — Clase Pila")
        self.configure(bg=BG)
        self.resizable(True, True)
        self.geometry("1000x700")
        self.minsize(800, 580)

        self._build_header()
        self._build_tabs()

    # ── Header ──────────────────────────────────────────────
    def _build_header(self):
        hdr = tk.Frame(self, bg=BG2, height=56)
        hdr.pack(fill="x")
        hdr.pack_propagate(False)

        tk.Label(hdr, text="◈  ESTRUCTURAS DE DATOS", font=FONT_TITLE,
                 bg=BG2, fg=ACCENT).pack(side="left", padx=20, pady=10)
        tk.Label(hdr, text="CLASE PILA", font=("Courier New", 10),
                 bg=BG2, fg=MUTED).pack(side="right", padx=20)

    # ── Tabs ────────────────────────────────────────────────
    def _build_tabs(self):
        style = ttk.Style(self)
        style.theme_use("clam")
        style.configure("TNotebook",           background=BG,  borderwidth=0)
        style.configure("TNotebook.Tab",       background=BG3, foreground=MUTED,
                        font=FONT_MONO_B, padding=(18, 8), borderwidth=0)
        style.map("TNotebook.Tab",
                  background=[("selected", BG2)],
                  foreground=[("selected", ACCENT2)])

        nb = ttk.Notebook(self)
        nb.pack(fill="both", expand=True, padx=0, pady=0)

        self.tab_hanoi = tk.Frame(nb, bg=BG)
        self.tab_eval  = tk.Frame(nb, bg=BG)

        nb.add(self.tab_hanoi, text="  🏛  Torres de Hanói  ")
        nb.add(self.tab_eval,  text="  ⚙  Evaluador de Expresiones  ")

        HanoiTab(self.tab_hanoi)
        EvaluadorTab(self.tab_eval)


# ════════════════════════════════════════════════════════════
#  TAB — TORRES DE HANÓI
# ════════════════════════════════════════════════════════════

class HanoiTab(tk.Frame):
    TOWER_NAMES = ['A', 'B', 'C']
    SPEED_MS    = 500   # ms entre movimientos

    def __init__(self, parent):
        super().__init__(parent, bg=BG)
        self.pack(fill="both", expand=True)

        self.n           = tk.IntVar(value=3)
        self.pilas       = {}
        self.movimientos = []
        self.paso        = 0
        self.animando    = False
        self._after_id   = None
        self.t_inicio    = 0.0
        self.t_final     = None
        self.timer_id    = None

        self._build()

    # ── UI ─────────────────────────────────────────────────
    def _build(self):
        # Panel izquierdo — controles
        ctrl = tk.Frame(self, bg=BG2, width=220)
        ctrl.pack(side="left", fill="y", padx=(8,0), pady=8)
        ctrl.pack_propagate(False)

        tk.Label(ctrl, text="CONFIGURACIÓN", font=FONT_SMALL,
                 bg=BG2, fg=MUTED).pack(pady=(18,4))

        tk.Label(ctrl, text="Número de discos:", font=FONT_MONO,
                 bg=BG2, fg=TEXT).pack(pady=(8,2))

        spin = tk.Spinbox(ctrl, from_=1, to=12, textvariable=self.n,
                          font=FONT_BIG, width=4, justify="center",
                          bg=BG3, fg=ACCENT2, insertbackground=ACCENT2,
                          buttonbackground=BG3, relief="flat",
                          highlightbackground=ACCENT, highlightthickness=1)
        spin.pack(pady=4)

        self.btn_iniciar = self._btn(ctrl, "▶  INICIAR", self._iniciar, ACCENT)
        self.btn_iniciar.pack(fill="x", padx=16, pady=(14,4))

        self.btn_paso = self._btn(ctrl, "⏭  PASO A PASO", self._un_paso, ACCENT2)
        self.btn_paso.pack(fill="x", padx=16, pady=4)
        self.btn_paso["state"] = "disabled"

        self.btn_auto = self._btn(ctrl, "⚡  AUTO", self._toggle_auto, WARNING)
        self.btn_auto.pack(fill="x", padx=16, pady=4)
        self.btn_auto["state"] = "disabled"

        self.btn_reset = self._btn(ctrl, "↺  RESET", self._reset, DANGER)
        self.btn_reset.pack(fill="x", padx=16, pady=(4,14))

        sep = tk.Frame(ctrl, bg=BG3, height=1)
        sep.pack(fill="x", padx=12, pady=6)

        # Stats
        tk.Label(ctrl, text="ESTADÍSTICAS", font=FONT_SMALL,
                 bg=BG2, fg=MUTED).pack(pady=(6,4))

        self.lbl_paso    = self._stat(ctrl, "Paso")
        self.lbl_total   = self._stat(ctrl, "Total movs")
        self.lbl_formula = self._stat(ctrl, "Fórmula")
        self.lbl_tiempo  = self._stat(ctrl, "Tiempo")

        sep2 = tk.Frame(ctrl, bg=BG3, height=1)
        sep2.pack(fill="x", padx=12, pady=10)

        # Log
        tk.Label(ctrl, text="LOG", font=FONT_SMALL,
                 bg=BG2, fg=MUTED).pack(pady=(0,4))

        log_frame = tk.Frame(ctrl, bg=BG3)
        log_frame.pack(fill="both", expand=True, padx=8, pady=(0,8))

        self.log = tk.Text(log_frame, font=("Courier New", 9),
                           bg=BG3, fg=MUTED, relief="flat",
                           state="disabled", wrap="none")
        scroll = tk.Scrollbar(log_frame, command=self.log.yview, bg=BG3)
        self.log.configure(yscrollcommand=scroll.set)
        scroll.pack(side="right", fill="y")
        self.log.pack(fill="both", expand=True, padx=4, pady=4)

        # Panel derecho — canvas
        right = tk.Frame(self, bg=BG)
        right.pack(side="left", fill="both", expand=True, padx=8, pady=8)

        self.lbl_mov = tk.Label(right, text="Configura y presiona INICIAR",
                                font=FONT_MONO_B, bg=BG, fg=ACCENT2)
        self.lbl_mov.pack(pady=(6,0))

        self.canvas = tk.Canvas(right, bg=BG, highlightthickness=0, width=600, height=400)
        self.canvas.pack(fill="both", expand=True)
        self.canvas.bind("<Configure>", lambda e: self._dibujar())

    def _btn(self, parent, text, cmd, color):
        return tk.Button(parent, text=text, command=cmd,
                         font=FONT_MONO_B, bg=BG3, fg=color,
                         activebackground=BG, activeforeground=color,
                         relief="flat", cursor="hand2",
                         highlightbackground=color, highlightthickness=1,
                         pady=7)

    def _stat(self, parent, label):
        f = tk.Frame(parent, bg=BG2)
        f.pack(fill="x", padx=12, pady=2)
        tk.Label(f, text=label + ":", font=FONT_SMALL, bg=BG2,
                 fg=MUTED, width=10, anchor="w").pack(side="left")
        lbl = tk.Label(f, text="—", font=FONT_SMALL, bg=BG2, fg=TEXT, anchor="w")
        lbl.pack(side="left")
        return lbl

    # ── Iniciar ─────────────────────────────────────────────
    def _iniciar(self):
        self._reset_state()
        n = self.n.get()

        # Crear pilas con la clase Pila
        for k in self.TOWER_NAMES:
            self.pilas[k] = Pila()
        for i in range(n, 0, -1):
            self.pilas['A'].apilar(i)

        self.movimientos = generar_movimientos(n)
        total = len(self.movimientos)

        self.lbl_total["text"]   = str(total)
        self.lbl_formula["text"] = f"2^{n}-1"
        self.lbl_paso["text"]    = f"0 / {total}"
        self.lbl_tiempo["text"]  = "—"

        self.btn_paso["state"] = "normal"
        self.btn_auto["state"] = "normal"

        self._log(f"Iniciado con {n} discos\n")
        self._log(f"Movimientos: {total}\n")
        self._dibujar()

    def _un_paso(self):
        if self.paso >= len(self.movimientos):
            return
        if self.paso == 0:
            self.t_inicio = time.perf_counter()
            self._iniciar_timer()

        disco, desde, hacia = self.movimientos[self.paso]
        elem = self.pilas[desde].desapilar()
        self.pilas[hacia].apilar(elem)

        self.paso += 1
        total = len(self.movimientos)
        self.lbl_paso["text"] = f"{self.paso} / {total}"
        self.lbl_mov.config(
            text=f"Paso {self.paso}:  Disco {disco}  ·  Torre {desde}  →  Torre {hacia}",
            fg=DISK_COLORS[(disco - 1) % len(DISK_COLORS)]
        )
        self._log(f"#{self.paso:>3}  Disco {disco}: {desde} → {hacia}\n")
        self._dibujar()

        if self.paso >= total:
            self._finalizar()

    def _toggle_auto(self):
        if self.animando:
            self.animando = False
            self.btn_auto.config(text="⚡  AUTO", fg=WARNING)
            if self._after_id:
                self.after_cancel(self._after_id)
        else:
            self.animando = True
            self.btn_auto.config(text="⏸  PAUSAR", fg=DANGER)
            self._auto_step()

    def _auto_step(self):
        if not self.animando:
            return
        if self.paso < len(self.movimientos):
            self._un_paso()
            self._after_id = self.after(self.SPEED_MS, self._auto_step)
        else:
            self.animando = False
            self.btn_auto.config(text="⚡  AUTO", fg=WARNING)

    def _finalizar(self):
        self.animando = False
        self.btn_auto.config(text="⚡  AUTO", fg=WARNING)
        self.btn_paso["state"] = "disabled"
        self.btn_auto["state"] = "disabled"
        self._detener_timer()
        elapsed = time.perf_counter() - self.t_inicio
        self.t_final = elapsed
        self.lbl_tiempo["text"] = f"{elapsed:.4f} s"
        self.lbl_mov.config(text="✓ ¡Completado!", fg=SUCCESS)
        self._log(f"\n✓ Completado en {elapsed:.6f} s\n")

    def _reset(self):
        if self._after_id:
            self.after_cancel(self._after_id)
        self._detener_timer()
        self._reset_state()
        self.lbl_mov.config(text="Configura y presiona INICIAR", fg=ACCENT2)
        self.canvas.delete("all")
        self._dibujar_vacias()

    def _reset_state(self):
        self.animando    = False
        self.paso        = 0
        self.movimientos = []
        self.pilas       = {}
        self.t_final     = None
        self.btn_auto.config(text="⚡  AUTO", fg=WARNING)
        self.btn_paso["state"] = "disabled"
        self.btn_auto["state"] = "disabled"
        self.lbl_paso["text"]    = "—"
        self.lbl_total["text"]   = "—"
        self.lbl_formula["text"] = "—"
        self.lbl_tiempo["text"]  = "—"
        self.log.config(state="normal")
        self.log.delete("1.0", "end")
        self.log.config(state="disabled")

    # ── Timer en vivo ───────────────────────────────────────
    def _iniciar_timer(self):
        self._detener_timer()
        self._tick_timer()

    def _tick_timer(self):
        if self.t_final is None and self.pilas:
            elapsed = time.perf_counter() - self.t_inicio
            self.lbl_tiempo["text"] = f"{elapsed:.3f} s"
            self.timer_id = self.after(100, self._tick_timer)

    def _detener_timer(self):
        if self.timer_id:
            self.after_cancel(self.timer_id)
            self.timer_id = None

    # ── Log ─────────────────────────────────────────────────
    def _log(self, msg):
        self.log.config(state="normal")
        self.log.insert("end", msg)
        self.log.see("end")
        self.log.config(state="disabled")

    # ── Dibujo Canvas ───────────────────────────────────────
    def _dibujar(self):
        self.canvas.update_idletasks()
        self.canvas.delete("all")
        w = self.canvas.winfo_width()
        h = self.canvas.winfo_height()
        if w < 50 or h < 50:
            self.after(50, self._dibujar)
            return

        n      = self.n.get()
        max_d  = max(n, 1)
        disk_h = max(20, min(34, (h - 140) // max(max_d, 1)))
        post_h = disk_h * max_d + 30
        base_y = h - 60
        post_w = 12

        # Cada torre ocupa 1/3 del ancho
        col_w  = w // 3
        max_dw = max(40, col_w - 40)
        min_dw = max(20, col_w // 6)

        # Centros X de cada torre — FIJO por columna
        cx = [col_w // 2 + i * col_w for i in range(3)]

        # Fondo
        self.canvas.create_rectangle(0, 0, w, h, fill=BG, outline="")

        # Línea de suelo
        self.canvas.create_line(20, base_y + 16, w - 20, base_y + 16,
                                fill="#2a2a4a", width=2)

        # ── Dibujar cada torre ──
        for idx, nombre in enumerate(self.TOWER_NAMES):
            x = cx[idx]

            # Base de la torre
            bw = min(col_w - 20, max_dw + 20)
            self.canvas.create_rectangle(
                x - bw // 2, base_y,
                x + bw // 2, base_y + 16,
                fill="#1e1e3a", outline=ACCENT, width=2
            )

            # Poste vertical
            self.canvas.create_rectangle(
                x - post_w // 2, base_y - post_h,
                x + post_w // 2, base_y,
                fill="#3a3a6a", outline="#5555aa", width=1
            )

            # Etiqueta
            self.canvas.create_text(
                x, base_y + 32,
                text=f"Torre {nombre}",
                font=("Courier New", 11, "bold"),
                fill=ACCENT2
            )

            # Discos
            discos = self.pilas[nombre].elementos if nombre in self.pilas else []
            for j, disco in enumerate(discos):
                ratio = (disco - 1) / max(max_d - 1, 1) if max_d > 1 else 1.0
                dw    = int(min_dw + ratio * (max_dw - min_dw))
                dy    = base_y - (j + 1) * (disk_h + 3)
                color = DISK_COLORS[(disco - 1) % len(DISK_COLORS)]

                # Sombra
                self.canvas.create_rectangle(
                    x - dw // 2 + 4, dy + 4,
                    x + dw // 2 + 4, dy + disk_h + 4,
                    fill="#000000", outline=""
                )
                # Cuerpo del disco
                self.canvas.create_rectangle(
                    x - dw // 2, dy,
                    x + dw // 2, dy + disk_h,
                    fill=color, outline="#222222", width=1
                )
                # Brillo superior
                self.canvas.create_rectangle(
                    x - dw // 2 + 4, dy + 3,
                    x + dw // 2 - 4, dy + disk_h // 3,
                    fill="#ffffff", outline="", stipple="gray25"
                )
                # Número disco
                self.canvas.create_text(
                    x, dy + disk_h // 2,
                    text=str(disco),
                    font=("Courier New", max(8, disk_h // 3), "bold"),
                    fill="#ffffff"
                )

        # Código Python del tiempo
        if self.paso > 0:
            elapsed = self.t_final if self.t_final else (time.perf_counter() - self.t_inicio)
            code = (f"import time\n"
                    f"inicio = time.perf_counter()\n"
                    f"hanoi(n={n})  # paso {self.paso}/{len(self.movimientos)}\n"
                    f"fin   = time.perf_counter()\n"
                    f"# tiempo = {elapsed:.6f} s")
            self.canvas.create_rectangle(
                8, 8, 345, 102,
                fill="#0d1117", outline="#30363d", width=1
            )
            self.canvas.create_text(
                16, 14, text=code,
                font=("Courier New", 8), fill="#79c0ff",
                anchor="nw", justify="left"
            )

    def _dibujar_vacias(self):
        self.canvas.delete("all")


# ════════════════════════════════════════════════════════════
#  TAB — EVALUADOR
# ════════════════════════════════════════════════════════════

class EvaluadorTab(tk.Frame):
    EJEMPLOS = {
        "postfija": [
            ("3 4 + 2 *",          "(3+4)×2 = 14"),
            ("5 1 2 + 4 * + 3 -",  "5+((1+2)×4)-3 = 14"),
            ("2 3 ** 4 -",         "2³-4 = 4"),
            ("15 7 1 1 + - / 3 *", "= 5"),
        ],
        "prefija": [
            ("* + 3 4 2",          "(3+4)×2 = 14"),
            ("- + 5 * + 1 2 4 3",  "5+((1+2)×4)-3 = 14"),
            ("- ** 2 3 4",         "2³-4 = 4"),
            ("* + 2 3 - 5 1",      "(2+3)×(5-1) = 20"),
        ],
    }

    def __init__(self, parent):
        super().__init__(parent, bg=BG)
        self.pack(fill="both", expand=True)
        self.modo = tk.StringVar(value="postfija")
        self._build()

    def _build(self):
        # Controles superiores
        top = tk.Frame(self, bg=BG2, height=56)
        top.pack(fill="x", padx=8, pady=(8, 0))
        top.pack_propagate(False)

        tk.Label(top, text="Notación:", font=FONT_MONO,
                 bg=BG2, fg=MUTED).pack(side="left", padx=(16, 8), pady=14)

        for val, lbl in [("postfija", "POSTFIJA (RPN)"), ("prefija", "PREFIJA (Polaca)")]:
            rb = tk.Radiobutton(top, text=lbl, variable=self.modo, value=val,
                                command=self._cambiar_modo,
                                font=FONT_MONO_B, bg=BG2, fg=ACCENT,
                                selectcolor=BG3, activebackground=BG2,
                                activeforeground=ACCENT2, cursor="hand2")
            rb.pack(side="left", padx=8)

        # Ejemplos
        ej_frame = tk.Frame(self, bg=BG)
        ej_frame.pack(fill="x", padx=8, pady=(4,0))
        tk.Label(ej_frame, text="Ejemplos:", font=FONT_SMALL,
                 bg=BG, fg=MUTED).pack(side="left", padx=(8,4))
        self.btn_ejs = []
        for i in range(4):
            b = tk.Button(ej_frame, text="", font=FONT_SMALL,
                          bg=BG3, fg=ACCENT2, relief="flat",
                          cursor="hand2", padx=8, pady=3,
                          activebackground=BG2, activeforeground=ACCENT2)
            b.pack(side="left", padx=3, pady=4)
            self.btn_ejs.append(b)
        self._actualizar_ejs()

        # Input
        inp_frame = tk.Frame(self, bg=BG)
        inp_frame.pack(fill="x", padx=8, pady=(4, 0))

        self.entry = tk.Entry(inp_frame, font=("Courier New", 14),
                              bg=BG3, fg=ACCENT2, insertbackground=ACCENT2,
                              relief="flat", highlightbackground=ACCENT,
                              highlightthickness=1)
        self.entry.pack(side="left", fill="x", expand=True, ipady=8, padx=(0,8))
        self.entry.insert(0, "3 4 + 2 *")
        self.entry.bind("<Return>", lambda e: self._evaluar())

        btn_eval = tk.Button(inp_frame, text="  EVALUAR  ",
                             command=self._evaluar,
                             font=FONT_MONO_B, bg=ACCENT, fg="#fff",
                             activebackground=ACCENT2, activeforeground="#000",
                             relief="flat", cursor="hand2", padx=12, pady=8)
        btn_eval.pack(side="left")

        # Resultado
        res_frame = tk.Frame(self, bg=BG2, height=72)
        res_frame.pack(fill="x", padx=8, pady=6)
        res_frame.pack_propagate(False)

        tk.Label(res_frame, text="RESULTADO:", font=FONT_MONO,
                 bg=BG2, fg=MUTED).pack(side="left", padx=20)
        self.lbl_resultado = tk.Label(res_frame, text="—",
                                      font=("Courier New", 32, "bold"),
                                      bg=BG2, fg=SUCCESS)
        self.lbl_resultado.pack(side="left", padx=12)
        self.lbl_error = tk.Label(res_frame, text="",
                                  font=FONT_MONO, bg=BG2, fg=DANGER)
        self.lbl_error.pack(side="left", padx=12)

        # Traza
        tk.Label(self, text="TRAZA DE LA PILA:", font=FONT_SMALL,
                 bg=BG, fg=MUTED).pack(anchor="w", padx=16, pady=(2,0))

        trace_frame = tk.Frame(self, bg=BG3)
        trace_frame.pack(fill="both", expand=True, padx=8, pady=(2,8))

        self.trace = tk.Text(trace_frame, font=("Courier New", 11),
                             bg=BG3, fg=TEXT, relief="flat",
                             state="disabled", wrap="none",
                             spacing1=4, spacing3=4)

        vsb = tk.Scrollbar(trace_frame, command=self.trace.yview, bg=BG3)
        hsb = tk.Scrollbar(trace_frame, command=self.trace.xview,
                           orient="horizontal", bg=BG3)
        self.trace.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)

        vsb.pack(side="right", fill="y")
        hsb.pack(side="bottom", fill="x")
        self.trace.pack(fill="both", expand=True, padx=6, pady=6)

        self.trace.tag_config("push",  foreground=ACCENT2)
        self.trace.tag_config("op",    foreground=WARNING)
        self.trace.tag_config("head",  foreground=MUTED)
        self.trace.tag_config("final", foreground=SUCCESS, font=("Courier New", 12, "bold"))

    def _actualizar_ejs(self):
        modo = self.modo.get()
        for i, (expr, desc) in enumerate(self.EJEMPLOS[modo]):
            btn = self.btn_ejs[i]
            btn.config(text=f"{expr}  ·  {desc}",
                       command=lambda e=expr: self._poner_ejemplo(e))

    def _cambiar_modo(self):
        self._actualizar_ejs()
        self.lbl_resultado.config(text="—")
        self.lbl_error.config(text="")
        self.trace.config(state="normal")
        self.trace.delete("1.0", "end")
        self.trace.config(state="disabled")

    def _poner_ejemplo(self, expr):
        self.entry.delete(0, "end")
        self.entry.insert(0, expr)
        self._evaluar()

    def _evaluar(self):
        expr = self.entry.get().strip()
        self.lbl_error.config(text="")
        self.lbl_resultado.config(text="—", fg=SUCCESS)
        self.trace.config(state="normal")
        self.trace.delete("1.0", "end")

        if not expr:
            self.lbl_error.config(text="⚠ Ingresa una expresión")
            self.trace.config(state="disabled")
            return

        try:
            fn = evaluar_postfija if self.modo.get() == "postfija" else evaluar_prefija
            resultado, pasos = fn(expr)

            val = int(resultado) if resultado == int(resultado) else round(resultado, 6)
            self.lbl_resultado.config(text=str(val), fg=SUCCESS)

            encabezado = (f"  Expresión : {expr}\n"
                          f"  Notación  : {self.modo.get().upper()}\n"
                          f"  {'─'*55}\n"
                          f"  {'Paso':<6} {'Acción':<45} {'Pila'}\n"
                          f"  {'─'*55}\n")
            self.trace.insert("end", encabezado, "head")

            for i, paso in enumerate(pasos, 1):
                tag = "op" if any(op in paso for op in ['→', '+', '-', '*', '/']) and "PUSH" not in paso.split()[0] else "push"
                self.trace.insert("end", f"  {i:<5} {paso}\n", tag)

            self.trace.insert("end", f"\n  {'─'*55}\n", "head")
            self.trace.insert("end", f"  ✓  RESULTADO = {val}\n", "final")

        except Exception as e:
            self.lbl_resultado.config(text="Error", fg=DANGER)
            self.lbl_error.config(text=f"✗  {e}")
            self.trace.insert("end", f"  Error: {e}\n")

        self.trace.config(state="disabled")


# ════════════════════════════════════════════════════════════
#  MAIN
# ════════════════════════════════════════════════════════════

if __name__ == "__main__":
    app = App()
    app.mainloop()