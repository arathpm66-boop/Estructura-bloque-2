"""
╔══════════════════════════════════════════════════════════════════════════════╗
║  LIBRERÍA DE ORDENAMIENTO INTERNO - CON GRÁFICAS EN TIEMPO REAL              ║
║  Visualiza cómo funciona cada algoritmo paso a paso                         ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""

import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import random
import json
import time
import pandas as pd
from docx import Document
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import threading
from typing import List, Optional, Generator

# ============================================
# CONFIGURACIÓN GLOBAL
# ============================================
velocidad = 0.3
fig = None
ax = None
animacion_activa = False

# ============================================
# VISUALIZACIÓN (SOLO UNA VENTANA)
# ============================================

def iniciar_grafico():
    """Inicializa la ventana de gráfico SOLO UNA VEZ"""
    global fig, ax
    if fig is None or not plt.fignum_exists(fig.number):
        plt.ion()
        fig, ax = plt.subplots(figsize=(14, 7))
        fig.canvas.manager.set_window_title('Visualizador de Ordenamientos - En Vivo')
        ax.set_title("Ordenamiento en progreso...")
        ax.set_xlabel("Posición")
        ax.set_ylabel("Valor")
    return fig, ax

def actualizar_grafico(datos, titulo, colores=None, idx_actual=None, idx_comp=None):
    """Actualiza el gráfico en la misma ventana"""
    global fig, ax
    
    if fig is None or not plt.fignum_exists(fig.number):
        fig, ax = iniciar_grafico()
    
    ax.clear()
    
    # Definir colores según el estado
    if colores is None:
        colores = []
        for i in range(len(datos)):
            if idx_actual is not None and i == idx_actual:
                colores.append('#ffd700')  # Dorado - elemento actual
            elif idx_comp is not None and i == idx_comp:
                colores.append('#ff6666')  # Rojo - elemento comparado
            else:
                colores.append('#4a90e2')  # Azul normal
    elif len(colores) != len(datos) and idx_actual is not None:
        # Si no se pasaron colores completos, generarlos automáticamente
        colores = []
        for i in range(len(datos)):
            if i == idx_actual:
                colores.append('#ffd700')
            elif i == idx_comp:
                colores.append('#ff6666')
            else:
                colores.append('#4a90e2')
    
    barras = ax.bar(range(len(datos)), datos, color=colores, edgecolor='white', linewidth=0.5)
    ax.set_title(titulo, fontsize=14, fontweight='bold', color='#2c3e50')
    ax.set_xlabel("Posición", fontsize=12)
    ax.set_ylabel("Valor", fontsize=12)
    ax.set_facecolor('#f0f0f0')
    fig.patch.set_facecolor('#f0f0f0')
    
    # Mostrar valores encima de las barras
    for i, barra in enumerate(barras):
        altura = barra.get_height()
        ax.text(barra.get_x() + barra.get_width()/2., altura,
                f'{int(altura)}', ha='center', va='bottom', fontsize=8, fontweight='bold')
    
    plt.tight_layout()
    plt.draw()
    plt.pause(velocidad)

def cerrar_grafico():
    """Cierra la ventana de gráfico"""
    global fig, animacion_activa
    animacion_activa = False
    if fig is not None:
        plt.close(fig)
        fig = None

# ============================================
# GENERADORES DE ALGORITMOS (paso a paso)
# ============================================

def generar_insertion_sort(datos):
    """Generador que muestra paso a paso el Insertion Sort"""
    arr = datos.copy()
    n = len(arr)
    
    yield arr.copy(), "Inicio - Lista original", None, None
    
    for i in range(1, n):
        clave = arr[i]
        j = i - 1
        
        yield arr.copy(), f"Tomando clave {clave} en posición {i}", i, None
        
        while j >= 0 and arr[j] > clave:
            yield arr.copy(), f"Comparando {clave} con {arr[j]} - {clave} < {arr[j]}, desplazando", j, i
            arr[j + 1] = arr[j]
            yield arr.copy(), f"Desplazado {arr[j+1]} a posición {j+1}", j, j+1
            j -= 1
        
        arr[j + 1] = clave
        yield arr.copy(), f"Insertando {clave} en posición {j+1}", j+1, None
    
    yield arr.copy(), "✅ Insertion Sort completado", None, None

def generar_bubble_sort(datos):
    """Generador que muestra paso a paso el Bubble Sort"""
    arr = datos.copy()
    n = len(arr)
    
    yield arr.copy(), "Inicio - Lista original", None, None
    
    for i in range(n - 1):
        intercambiado = False
        for j in range(0, n - i - 1):
            yield arr.copy(), f"Comparando {arr[j]} y {arr[j+1]}", j, j+1
            
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                intercambiado = True
                yield arr.copy(), f"Intercambiando {arr[j+1]} ↔ {arr[j]}", j, j+1
        
        if not intercambiado:
            break
    
    yield arr.copy(), "✅ Bubble Sort completado", None, None

def generar_selection_sort(datos):
    """Generador que muestra paso a paso el Selection Sort"""
    arr = datos.copy()
    n = len(arr)
    
    yield arr.copy(), "Inicio - Lista original", None, None
    
    for i in range(n - 1):
        idx_min = i
        
        for j in range(i + 1, n):
            yield arr.copy(), f"Buscando mínimo - actual mínimo: {arr[idx_min]} en pos {idx_min}", idx_min, j
            
            if arr[j] < arr[idx_min]:
                idx_min = j
                yield arr.copy(), f"Nuevo mínimo encontrado: {arr[idx_min]} en pos {idx_min}", idx_min, None
        
        if idx_min != i:
            arr[i], arr[idx_min] = arr[idx_min], arr[i]
            yield arr.copy(), f"Intercambiando {arr[i]} (pos {i}) ↔ {arr[idx_min]} (pos {idx_min})", i, idx_min
    
    yield arr.copy(), "✅ Selection Sort completado", None, None

def generar_shell_sort(datos):
    """Generador que muestra paso a paso el Shell Sort"""
    arr = datos.copy()
    n = len(arr)
    gap = n // 2
    
    yield arr.copy(), "Inicio - Lista original", None, None
    
    while gap > 0:
        yield arr.copy(), f"Gap actual: {gap} - Ordenando sublistas separadas por {gap} espacios", None, None
        
        for i in range(gap, n):
            clave = arr[i]
            j = i
            
            yield arr.copy(), f"Comparando elemento {clave} en pos {i} con elementos a {gap} espacios", i, j-gap if j>=gap else None
            
            while j >= gap and arr[j - gap] > clave:
                arr[j] = arr[j - gap]
                yield arr.copy(), f"Desplazando {arr[j-gap]} a posición {j}", j, j-gap
                j -= gap
            
            arr[j] = clave
            yield arr.copy(), f"Insertando {clave} en posición {j}", j, None
        
        gap //= 2
    
    yield arr.copy(), "✅ Shell Sort completado", None, None

def generar_quick_sort(datos):
    """Generador que muestra paso a paso el Quick Sort"""
    arr = datos.copy()
    
    def quick_sort_rec(arr, bajo, alto):
        if bajo < alto:
            # Partición
            pivote = arr[alto]
            i = bajo - 1
            
            yield arr.copy(), f"Pivote: {pivote} en posición {alto} - Partición", alto, None
            
            for j in range(bajo, alto):
                yield arr.copy(), f"Comparando {arr[j]} con pivote {pivote}", j, alto
                if arr[j] <= pivote:
                    i += 1
                    arr[i], arr[j] = arr[j], arr[i]
                    if i != j:
                        yield arr.copy(), f"Intercambiando {arr[i]} y {arr[j]}", i, j
            
            arr[i + 1], arr[alto] = arr[alto], arr[i + 1]
            yield arr.copy(), f"Pivote {pivote} colocado en posición {i+1}", i+1, None
            
            # Recursión
            yield from quick_sort_rec(arr, bajo, i)
            yield from quick_sort_rec(arr, i + 2, alto)
    
    yield arr.copy(), "Inicio - Quick Sort", None, None
    yield from quick_sort_rec(arr, 0, len(arr) - 1)
    yield arr.copy(), "✅ Quick Sort completado", None, None

def generar_heap_sort(datos):
    """Generador que muestra paso a paso el Heap Sort"""
    arr = datos.copy()
    n = len(arr)
    
    def heapify(arr, n, i):
        mayor = i
        izq = 2 * i + 1
        der = 2 * i + 2
        
        if izq < n and arr[izq] > arr[mayor]:
            mayor = izq
        if der < n and arr[der] > arr[mayor]:
            mayor = der
        
        if mayor != i:
            arr[i], arr[mayor] = arr[mayor], arr[i]
            yield arr.copy(), f"Heapify: {arr[i]} sube a raíz", i, mayor
            yield from heapify(arr, n, mayor)
    
    # Construir heap
    yield arr.copy(), "Construyendo Max-Heap", None, None
    for i in range(n // 2 - 1, -1, -1):
        yield from heapify(arr, n, i)
    
    # Extraer elementos
    yield arr.copy(), "Heap construido - Extrayendo elementos", None, None
    for i in range(n - 1, 0, -1):
        arr[0], arr[i] = arr[i], arr[0]
        yield arr.copy(), f"Extrayendo máximo {arr[i]} a posición {i}", 0, i
        yield from heapify(arr, i, 0)
    
    yield arr.copy(), "✅ Heap Sort completado", None, None

def generar_radix_sort(datos):
    """Generador que muestra paso a paso el Radix Sort"""
    if any(x < 0 for x in datos):
        raise ValueError("Radix Sort solo funciona con números no negativos")
    
    arr = datos.copy()
    if not arr:
        yield arr, "Lista vacía", None, None
        return
    
    max_val = max(arr)
    exp = 1
    paso = 1
    
    yield arr.copy(), "Inicio - Radix Sort (por dígitos)", None, None
    
    while max_val // exp > 0:
        n = len(arr)
        salida = [0] * n
        conteo = [0] * 10
        
        yield arr.copy(), f"Paso {paso} - Ordenando por dígito posición {exp}", None, None
        
        # Contar ocurrencias
        for num in arr:
            digito = (num // exp) % 10
            conteo[digito] += 1
        
        # Conteo acumulado
        for i in range(1, 10):
            conteo[i] += conteo[i - 1]
        
        # Construir salida
        for i in range(n - 1, -1, -1):
            digito = (arr[i] // exp) % 10
            salida[conteo[digito] - 1] = arr[i]
            conteo[digito] -= 1
            yield salida.copy(), f"Colocando {arr[i]} según su dígito {digito}", i, None
        
        # Copiar resultado
        for i in range(n):
            arr[i] = salida[i]
        
        yield arr.copy(), f"Paso {paso} completado - Ordenado por dígito {exp}", None, None
        
        exp *= 10
        paso += 1
    
    yield arr.copy(), "✅ Radix Sort completado", None, None

# ============================================
# LECTORES DE ARCHIVOS
# ============================================

def leer_txt(ruta):
    with open(ruta, 'r', encoding='utf-8') as f:
        return list(map(int, f.read().split()))

def leer_json(ruta):
    with open(ruta, 'r', encoding='utf-8') as f:
        data = json.load(f)
    if "datos" in data:
        return data["datos"]
    elif "numeros" in data:
        return data["numeros"]
    else:
        for key, value in data.items():
            if isinstance(value, list):
                return value
        raise ValueError("JSON debe contener una lista")

def leer_word(ruta):
    doc = Document(ruta)
    texto = " ".join(p.text for p in doc.paragraphs)
    return list(map(int, texto.split()))

def leer_excel(ruta):
    xls = pd.ExcelFile(ruta)
    for hoja in xls.sheet_names:
        df = pd.read_excel(xls, sheet_name=hoja)
        datos = df.select_dtypes(include='number').values.flatten()
        datos = [int(x) for x in datos if not pd.isna(x)]
        if datos:
            return datos
    raise ValueError("Excel sin datos numéricos")

# ============================================
# CLASE PRINCIPAL CON GRÁFICAS
# ============================================

class AppGrafica:
    def __init__(self, root):
        self.root = root
        self.root.title("📊 Visualizador de Ordenamientos - En Vivo")
        self.root.geometry("900x750")
        self.root.configure(bg='#1a1a2e')
        
        self.datos = []
        self.animacion_ejecutando = False
        self.generador_actual = None
        
        self.metodos = {
            "🔵 Inserción (Insertion Sort)": generar_insertion_sort,
            "🟠 Burbuja (Bubble Sort)": generar_bubble_sort,
            "🟣 Selección (Selection Sort)": generar_selection_sort,
            "🔷 Shell Sort": generar_shell_sort,
            "🟢 Quick Sort": generar_quick_sort,
            "🟤 Heap Sort": generar_heap_sort,
            "🔴 Radix Sort": generar_radix_sort
        }
        
        self._build_ui()
        self.root.protocol("WM_DELETE_WINDOW", self._on_closing)
    
    def _build_ui(self):
        # Título
        tk.Label(self.root, text="📊 VISUALIZADOR DE ORDENAMIENTOS - EN VIVO", 
                font=("Arial", 18, "bold"), bg='#1a1a2e', fg='#00ff88').pack(pady=10)
        tk.Label(self.root, text="Observa paso a paso cómo funciona cada algoritmo", 
                font=("Arial", 10), bg='#1a1a2e', fg='#aaaaaa').pack()
        
        # Frame de carga
        frame_carga = tk.LabelFrame(self.root, text="📁 CARGAR DATOS", 
                                    bg='#16213e', fg='white', font=("Arial", 11, "bold"))
        frame_carga.pack(fill=tk.X, padx=20, pady=10)
        
        # Entrada manual
        tk.Label(frame_carga, text="Números (separados por coma o espacio):", 
                bg='#16213e', fg='white').pack(anchor=tk.W, padx=10)
        self.entry = tk.Entry(frame_carga, width=80, font=("Consolas", 10))
        self.entry.pack(padx=10, pady=5)
        
        # Botones de carga
        frame_botones = tk.Frame(frame_carga, bg='#16213e')
        frame_botones.pack(pady=5)
        
        botones = [
            ("📄 TXT", self.cargar_txt), ("📦 JSON", self.cargar_json),
            ("📝 Word", self.cargar_word), ("📊 Excel", self.cargar_excel),
            ("🎲 Random (15 nums)", self.generar_random),
            ("✅ Usar Manual", self.usar_manual)
        ]
        
        for texto, comando in botones:
            tk.Button(frame_botones, text=texto, command=comando,
                     bg='#0f3460', fg='white', padx=10).pack(side=tk.LEFT, padx=5)
        
        # Label datos
        self.label_datos = tk.Label(frame_carga, text="📊 Sin datos cargados", 
                                    bg='#16213e', fg='#ffd700', font=("Consolas", 9))
        self.label_datos.pack(pady=5)
        
        # Frame de algoritmo
        frame_algo = tk.LabelFrame(self.root, text="🎯 SELECCIONAR ALGORITMO", 
                                   bg='#16213e', fg='white', font=("Arial", 11, "bold"))
        frame_algo.pack(fill=tk.X, padx=20, pady=10)
        
        tk.Label(frame_algo, text="Método:", bg='#16213e', fg='white').pack(side=tk.LEFT, padx=10)
        self.metodo_var = tk.StringVar(value="🔵 Inserción (Insertion Sort)")
        combo = ttk.Combobox(frame_algo, textvariable=self.metodo_var, 
                             values=list(self.metodos.keys()), state="readonly", width=30)
        combo.pack(side=tk.LEFT, padx=10)
        
        # Botones de control
        self.btn_visualizar = tk.Button(frame_algo, text="🎬 VISUALIZAR", command=self.visualizar,
                                        bg='#00ff88', fg='#1a1a2e', font=("Arial", 11, "bold"), padx=20)
        self.btn_visualizar.pack(side=tk.LEFT, padx=20)
        
        self.btn_detener = tk.Button(frame_algo, text="⏹️ DETENER", command=self.detener,
                                     bg='#e94560', fg='white', font=("Arial", 11, "bold"), padx=20, state=tk.DISABLED)
        self.btn_detener.pack(side=tk.LEFT, padx=10)
        
        # Control de velocidad
        frame_vel = tk.Frame(frame_algo, bg='#16213e')
        frame_vel.pack(side=tk.LEFT, padx=20)
        tk.Label(frame_vel, text="Velocidad:", bg='#16213e', fg='white').pack(side=tk.LEFT)
        self.vel_var = tk.DoubleVar(value=0.3)
        self.vel_scale = tk.Scale(frame_vel, from_=0.05, to=1.0, resolution=0.05,
                                  orient=tk.HORIZONTAL, variable=self.vel_var,
                                  length=150, bg='#16213e', fg='white', command=self._cambiar_vel)
        self.vel_scale.pack(side=tk.LEFT, padx=5)
        
        # Frame de información
        frame_info = tk.LabelFrame(self.root, text="ℹ️ INFORMACIÓN DEL ALGORITMO", 
                                   bg='#16213e', fg='white', font=("Arial", 11, "bold"))
        frame_info.pack(fill=tk.X, padx=20, pady=10)
        
        self.label_info = tk.Label(frame_info, text="Selecciona un algoritmo y haz clic en VISUALIZAR", 
                                   bg='#16213e', fg='#00ff88', font=("Arial", 10))
        self.label_info.pack(pady=10)
        
        # Estado
        self.label_status = tk.Label(self.root, text="✅ Listo | Elige un algoritmo y visualiza", 
                                     bg='#1a1a2e', fg='#00ff88')
        self.label_status.pack(pady=5)
    
    def _cambiar_vel(self, val):
        global velocidad
        velocidad = self.vel_var.get()
    
    def actualizar_label_datos(self):
        if self.datos:
            mostrar = str(self.datos[:20])
            if len(self.datos) > 20:
                mostrar += f"... (+{len(self.datos)-20} más)"
            self.label_datos.config(text=f"📊 {len(self.datos)} elementos: {mostrar}")
        else:
            self.label_datos.config(text="📊 Sin datos cargados")
    
    def _on_closing(self):
        self.detener()
        cerrar_grafico()
        self.root.destroy()
    
    def cargar_txt(self):
        ruta = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
        if ruta:
            try:
                self.datos = leer_txt(ruta)
                self.actualizar_label_datos()
                messagebox.showinfo("Éxito", f"Cargados {len(self.datos)} números")
            except Exception as e:
                messagebox.showerror("Error", str(e))
    
    def cargar_json(self):
        ruta = filedialog.askopenfilename(filetypes=[("JSON files", "*.json")])
        if ruta:
            try:
                self.datos = leer_json(ruta)
                self.actualizar_label_datos()
                messagebox.showinfo("Éxito", f"Cargados {len(self.datos)} números")
            except Exception as e:
                messagebox.showerror("Error", str(e))
    
    def cargar_word(self):
        ruta = filedialog.askopenfilename(filetypes=[("Word files", "*.docx")])
        if ruta:
            try:
                self.datos = leer_word(ruta)
                self.actualizar_label_datos()
                messagebox.showinfo("Éxito", f"Cargados {len(self.datos)} números")
            except Exception as e:
                messagebox.showerror("Error", str(e))
    
    def cargar_excel(self):
        ruta = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx")])
        if ruta:
            try:
                self.datos = leer_excel(ruta)
                self.actualizar_label_datos()
                messagebox.showinfo("Éxito", f"Cargados {len(self.datos)} números")
            except Exception as e:
                messagebox.showerror("Error", str(e))
    
    def generar_random(self):
        cantidad = 15
        self.datos = [random.randint(1, 100) for _ in range(cantidad)]
        self.actualizar_label_datos()
        messagebox.showinfo("Random", f"Generados {cantidad} números aleatorios")
    
    def usar_manual(self):
        try:
            texto = self.entry.get()
            texto = texto.replace(',', ' ')
            self.datos = list(map(int, texto.split()))
            self.actualizar_label_datos()
            messagebox.showinfo("Manual", f"Datos cargados: {self.datos[:20]}")
        except Exception as e:
            messagebox.showerror("Error", "Ingresa números válidos separados por espacios o comas")
    
    def visualizar(self):
        if not self.datos:
            messagebox.showerror("Error", "Primero carga o genera datos")
            return
        
        if len(self.datos) > 50:
            if not messagebox.askyesno("Advertencia", f"Tienes {len(self.datos)} elementos.\n¿Seguro que quieres visualizar? Puede ser lento."):
                return
        
        metodo_nombre = self.metodo_var.get()
        generador_func = self.metodos[metodo_nombre]
        
        # Información del algoritmo
        info_algoritmos = {
            "Inserción": "O(n²) - Bueno para listas pequeñas o casi ordenadas",
            "Burbuja": "O(n²) - Simple pero ineficiente en listas grandes",
            "Selección": "O(n²) - Hace pocos intercambios",
            "Shell": "O(n log² n) - Mejora del Insertion Sort",
            "Quick": "O(n log n) - Muy rápido en la práctica",
            "Heap": "O(n log n) - Rendimiento garantizado",
            "Radix": "O(nk) - Excelente para enteros"
        }
        
        for clave, info in info_algoritmos.items():
            if clave in metodo_nombre:
                self.label_info.config(text=f"📖 {metodo_nombre} | Complejidad: {info}")
                break
        
        self.animacion_ejecutando = True
        self.btn_visualizar.config(state=tk.DISABLED)
        self.btn_detener.config(state=tk.NORMAL)
        
        self.label_status.config(text=f"🔄 Visualizando {metodo_nombre}...")
        
        def ejecutar():
            try:
                generador = generador_func(self.datos)
                
                for datos_paso, mensaje, idx_actual, idx_comp in generador:
                    if not self.animacion_ejecutando:
                        break
                    
                    iniciar_grafico()
                    actualizar_grafico(datos_paso, mensaje, None, idx_actual, idx_comp)
                    time.sleep(velocidad)
                
                if self.animacion_ejecutando:
                    self.root.after(0, lambda: self.label_status.config(text="✅ Visualización completada"))
                else:
                    self.root.after(0, lambda: self.label_status.config(text="⏹️ Visualización detenida"))
            
            except Exception as e:
                self.root.after(0, lambda: messagebox.showerror("Error", str(e)))
                self.root.after(0, lambda: self.label_status.config(text="❌ Error en la visualización"))
            
            finally:
                self.root.after(0, self._finalizar_visualizacion)
        
        thread = threading.Thread(target=ejecutar, daemon=True)
        thread.start()
    
    def detener(self):
        self.animacion_ejecutando = False
    
    def _finalizar_visualizacion(self):
        self.animacion_ejecutando = False
        self.btn_visualizar.config(state=tk.NORMAL)
        self.btn_detener.config(state=tk.DISABLED)
        self.label_status.config(text="✅ Listo | Elige un algoritmo y visualiza")

# ============================================
# MAIN
# ============================================

if __name__ == "__main__":
    print("=" * 60)
    print("📊 VISUALIZADOR DE ORDENAMIENTOS - EN VIVO")
    print("✅ 7 algoritmos con visualización paso a paso")
    print("✅ Lectura: TXT, JSON, Word, Excel")
    print("✅ Control de velocidad")
    print("=" * 60)
    
    root = tk.Tk()
    app = AppGrafica(root)
    root.mainloop()