"""
╔══════════════════════════════════════════════════════════════════════════════╗
║  PROGRAMA DE PRUEBA - VERSIÓN CORREGIDA                                      ║
║  Maneja correctamente los generadores de tu librería interna                 ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import time
import random
import os
import sys

# ============================================
# IMPORTAR LIBRERÍAS
# ============================================

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Diccionarios
LECTORES = {}
ALGORITMOS_MEDIR = {}  # Para medir tiempo
ALGORITMOS_VISUALES = {}  # Para visualización
EXTERNO_FUNC = None

# ============================================
# 1. IMPORTAR LIBRERÍA EXTERNA
# ============================================
try:
    import ordenamientos_externo_libreria as ext
    
    # Lectores
    if hasattr(ext, 'leer_txt'):
        LECTORES['txt'] = ext.leer_txt
    if hasattr(ext, 'leer_json'):
        LECTORES['json'] = ext.leer_json
    if hasattr(ext, 'leer_word'):
        LECTORES['word'] = ext.leer_word
    if hasattr(ext, 'leer_excel'):
        LECTORES['excel'] = ext.leer_excel
    
    # Ordenamiento externo
    if hasattr(ext, 'ordenamiento_externo_mezcla'):
        EXTERNO_FUNC = ext.ordenamiento_externo_mezcla
    
    # Algoritmos de la librería externa (versiones para medir tiempo)
    if hasattr(ext, 'intercalacion'):
        ALGORITMOS_MEDIR['Inserción (intercalacion)'] = ext.intercalacion
    if hasattr(ext, 'mezcla_directa'):
        ALGORITMOS_MEDIR['Mezcla Directa (merge sort)'] = ext.mezcla_directa
    if hasattr(ext, 'mezcla_equilibrada'):
        ALGORITMOS_MEDIR['Mezcla Equilibrada'] = ext.mezcla_equilibrada
    
    print("✅ Librería EXTERNA cargada")
    print(f"   Lectores: {list(LECTORES.keys())}")
    
except Exception as e:
    print(f"⚠️ Error externa: {e}")

# ============================================
# 2. IMPORTAR LIBRERÍA INTERNA (GENERADORES PARA VISUALIZACIÓN)
# ============================================
try:
    import ordenamiento_interno_Libreria as inter
    
    # Guardar los generadores para visualización (pero no para medir tiempo)
    if hasattr(inter, 'generar_insertion_sort'):
        ALGORITMOS_VISUALES['Insertion Sort'] = inter.generar_insertion_sort
    if hasattr(inter, 'generar_bubble_sort'):
        ALGORITMOS_VISUALES['Bubble Sort'] = inter.generar_bubble_sort
    if hasattr(inter, 'generar_selection_sort'):
        ALGORITMOS_VISUALES['Selection Sort'] = inter.generar_selection_sort
    if hasattr(inter, 'generar_shell_sort'):
        ALGORITMOS_VISUALES['Shell Sort'] = inter.generar_shell_sort
    if hasattr(inter, 'generar_quick_sort'):
        ALGORITMOS_VISUALES['Quick Sort'] = inter.generar_quick_sort
    if hasattr(inter, 'generar_heap_sort'):
        ALGORITMOS_VISUALES['Heap Sort'] = inter.generar_heap_sort
    if hasattr(inter, 'generar_radix_sort'):
        ALGORITMOS_VISUALES['Radix Sort'] = inter.generar_radix_sort
    
    print(f"✅ Librería INTERNA cargada: {len(ALGORITMOS_VISUALES)} generadores")
    
except Exception as e:
    print(f"⚠️ Error interna: {e}")

# ============================================
# 3. FUNCIONES DE ORDENAMIENTO PARA MEDIR TIEMPO (versiones rápidas)
# ============================================

def quick_sort_medir(arr):
    """Quick Sort - versión para medir tiempo"""
    if len(arr) <= 1:
        return arr
    pivote = arr[-1]
    menores = [x for x in arr[:-1] if x <= pivote]
    mayores = [x for x in arr[:-1] if x > pivote]
    return quick_sort_medir(menores) + [pivote] + quick_sort_medir(mayores)

def heap_sort_medir(arr):
    """Heap Sort - versión para medir tiempo"""
    datos = arr[:]
    n = len(datos)
    
    def heapify(datos, n, i):
        mayor = i
        izq = 2 * i + 1
        der = 2 * i + 2
        if izq < n and datos[izq] > datos[mayor]:
            mayor = izq
        if der < n and datos[der] > datos[mayor]:
            mayor = der
        if mayor != i:
            datos[i], datos[mayor] = datos[mayor], datos[i]
            heapify(datos, n, mayor)
    
    for i in range(n // 2 - 1, -1, -1):
        heapify(datos, n, i)
    
    for i in range(n - 1, 0, -1):
        datos[0], datos[i] = datos[i], datos[0]
        heapify(datos, i, 0)
    
    return datos

def radix_sort_medir(arr):
    """Radix Sort - versión para medir tiempo"""
    if any(x < 0 for x in arr):
        raise ValueError("Radix Sort solo funciona con números positivos")
    datos = arr[:]
    if not datos:
        return datos
    maximo = max(datos)
    exp = 1
    while maximo // exp > 0:
        n = len(datos)
        salida = [0] * n
        conteo = [0] * 10
        for num in datos:
            digito = (num // exp) % 10
            conteo[digito] += 1
        for i in range(1, 10):
            conteo[i] += conteo[i - 1]
        for i in range(n - 1, -1, -1):
            digito = (datos[i] // exp) % 10
            salida[conteo[digito] - 1] = datos[i]
            conteo[digito] -= 1
        for i in range(n):
            datos[i] = salida[i]
        exp *= 10
    return datos

# Agregar a las funciones de medición
ALGORITMOS_MEDIR['Quick Sort (rápido)'] = quick_sort_medir
ALGORITMOS_MEDIR['Heap Sort (rápido)'] = heap_sort_medir
ALGORITMOS_MEDIR['Radix Sort (rápido)'] = radix_sort_medir

# ============================================
# 4. FUNCIÓN PARA EXTRAER EL RESULTADO DE UN GENERADOR
# ============================================

def ejecutar_generador_y_obtener_resultado(generador_func, datos):
    """
    Ejecuta un generador paso a paso y devuelve el último estado (ordenado)
    """
    gen = generador_func(datos)
    ultimo_datos = datos
    for datos_paso, mensaje, idx_actual, idx_comp in gen:
        ultimo_datos = datos_paso
    return ultimo_datos

# ============================================
# PROGRAMA PRINCIPAL
# ============================================

class AppPruebaFinal(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("📊 PROGRAMA DE PRUEBA - Tus Librerías")
        self.geometry("1200x850")
        self.configure(bg='#1a1a2e')
        
        self.datos = []
        
        self._build_ui()
        self._bienvenida()
    
    def _build_ui(self):
        # Título
        titulo = tk.Label(self, text="📊 PROGRAMA DE PRUEBA - LIBRERÍAS DE ORDENAMIENTO", 
                         font=("Arial", 16, "bold"), bg='#1a1a2e', fg='#00ff88')
        titulo.pack(pady=10)
        
        info = f"🔹 Para medir tiempo: {len(ALGORITMOS_MEDIR)} | 🔹 Para visualizar: {len(ALGORITMOS_VISUALES)} | 🔹 Lectores: {len(LECTORES)}"
        tk.Label(self, text=info, font=("Arial", 10), bg='#1a1a2e', fg='#aaaaaa').pack()
        
        # Frame superior - Carga de datos
        frame_carga = tk.LabelFrame(self, text="📁 CARGA DE DATOS", 
                                    bg='#16213e', fg='white', font=("Arial", 11, "bold"))
        frame_carga.pack(fill=tk.X, padx=15, pady=10)
        
        tk.Label(frame_carga, text="Números (separados por coma o espacio):", 
                bg='#16213e', fg='white').pack(anchor=tk.W, padx=10)
        self.entry = tk.Entry(frame_carga, width=80, font=("Consolas", 10))
        self.entry.pack(padx=10, pady=5)
        
        frame_botones = tk.Frame(frame_carga, bg='#16213e')
        frame_botones.pack(pady=5)
        
        # Botones de carga
        if 'txt' in LECTORES:
            tk.Button(frame_botones, text="📄 TXT", command=self.cargar_txt,
                     bg='#0f3460', fg='white', padx=12).pack(side=tk.LEFT, padx=5)
        if 'json' in LECTORES:
            tk.Button(frame_botones, text="📦 JSON", command=self.cargar_json,
                     bg='#0f3460', fg='white', padx=12).pack(side=tk.LEFT, padx=5)
        if 'word' in LECTORES:
            tk.Button(frame_botones, text="📝 Word", command=self.cargar_word,
                     bg='#0f3460', fg='white', padx=12).pack(side=tk.LEFT, padx=5)
        if 'excel' in LECTORES:
            tk.Button(frame_botones, text="📊 Excel", command=self.cargar_excel,
                     bg='#0f3460', fg='white', padx=12).pack(side=tk.LEFT, padx=5)
        
        tk.Button(frame_botones, text="🎲 Random (20 nums)", command=self.generar_random,
                 bg='#0f3460', fg='white', padx=12).pack(side=tk.LEFT, padx=5)
        tk.Button(frame_botones, text="✏️ Manual", command=self.usar_manual,
                 bg='#0f3460', fg='white', padx=12).pack(side=tk.LEFT, padx=5)
        
        self.label_datos = tk.Label(frame_carga, text="📊 Sin datos cargados", 
                                    bg='#16213e', fg='#ffd700', font=("Consolas", 10))
        self.label_datos.pack(pady=5)
        
        # Notebook para pestañas
        notebook = ttk.Notebook(self)
        notebook.pack(fill=tk.BOTH, expand=True, padx=15, pady=10)
        
        # ========== PESTAÑA 1: MEDIR TIEMPO ==========
        tab_medir = tk.Frame(notebook, bg='#16213e')
        notebook.add(tab_medir, text="⏱️ MEDIR TIEMPO")
        
        self._build_tab_medir(tab_medir)
        
        # ========== PESTAÑA 2: VISUALIZACIÓN ==========
        tab_visual = tk.Frame(notebook, bg='#16213e')
        notebook.add(tab_visual, text="🎬 VISUALIZACIÓN")
        
        self._build_tab_visual(tab_visual)
        
        # ========== PESTAÑA 3: COMPARATIVA ==========
        tab_comp = tk.Frame(notebook, bg='#16213e')
        notebook.add(tab_comp, text="📊 COMPARATIVA")
        
        self._build_tab_comparativa(tab_comp)
        
        # Estado
        self.label_status = tk.Label(self, text="✅ Listo | Carga datos y selecciona una opción", 
                                     bg='#1a1a2e', fg='#00ff88')
        self.label_status.pack(pady=5)
    
    def _build_tab_medir(self, parent):
        """Pestaña para medir tiempo de algoritmos"""
        # Panel izquierdo - lista de algoritmos
        frame_lista = tk.LabelFrame(parent, text="🧠 ALGORITMOS PARA MEDIR", 
                                    bg='#16213e', fg='white', font=("Arial", 11, "bold"))
        frame_lista.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Canvas con scroll
        canvas = tk.Canvas(frame_lista, bg='#16213e', highlightthickness=0)
        scrollbar = tk.Scrollbar(frame_lista, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg='#16213e')
        
        scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        for nombre in sorted(ALGORITMOS_MEDIR.keys()):
            btn = tk.Button(scrollable_frame, text=nombre, 
                           command=lambda n=nombre: self.ejecutar_medir(n),
                           bg='#2d2d44', fg='white', width=35, pady=5, font=("Arial", 9))
            btn.pack(pady=3)
        
        if EXTERNO_FUNC:
            tk.Label(scrollable_frame, text="━━━━━━━━━━━━━━━━━━━━━━", 
                    bg='#16213e', fg='#5c3d6e').pack(pady=5)
            btn_ext = tk.Button(scrollable_frame, text="💾 ORDENAMIENTO EXTERNO", 
                               command=self.ejecutar_externo,
                               bg='#5c3d6e', fg='white', width=35, pady=5, font=("Arial", 10, "bold"))
            btn_ext.pack(pady=3)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Panel derecho - resultados
        frame_resultados = tk.LabelFrame(parent, text="📋 RESULTADOS", 
                                         bg='#16213e', fg='white', font=("Arial", 11, "bold"))
        frame_resultados.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        text_frame = tk.Frame(frame_resultados, bg='#16213e')
        text_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        scroll_texto = tk.Scrollbar(text_frame)
        self.text_medir = tk.Text(text_frame, yscrollcommand=scroll_texto.set,
                                  bg='#0f3460', fg='#00ff88', font=("Consolas", 10), wrap=tk.WORD)
        scroll_texto.config(command=self.text_medir.yview)
        
        self.text_medir.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scroll_texto.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.text_medir.tag_config("verde", foreground="#00ff88")
        self.text_medir.tag_config("amarillo", foreground="#ffd700")
        self.text_medir.tag_config("rojo", foreground="#ff6666")
        self.text_medir.tag_config("azul", foreground="#66b3ff")
    
    def _build_tab_visual(self, parent):
        """Pestaña para visualización (usa los generadores)"""
        frame_info = tk.LabelFrame(parent, text="🎬 VISUALIZACIÓN PASO A PASO", 
                                   bg='#16213e', fg='white', font=("Arial", 11, "bold"))
        frame_info.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        tk.Label(frame_info, text="Los algoritmos de visualización abren una ventana de matplotlib\n"
                 "para mostrar el proceso paso a paso.", 
                bg='#16213e', fg='#00ff88', font=("Arial", 12)).pack(pady=20)
        
        # Botones para cada visualización
        frame_botones = tk.Frame(frame_info, bg='#16213e')
        frame_botones.pack(pady=20)
        
        for nombre in sorted(ALGORITMOS_VISUALES.keys()):
            btn = tk.Button(frame_botones, text=f"🎬 Visualizar {nombre}", 
                           command=lambda n=nombre: self.ejecutar_visualizar(n),
                           bg='#2d2d44', fg='white', width=25, pady=8, font=("Arial", 10))
            btn.pack(pady=5)
    
    def _build_tab_comparativa(self, parent):
        """Pestaña para comparativa de todos los algoritmos"""
        frame_comp = tk.Frame(parent, bg='#16213e')
        frame_comp.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        btn_comparar = tk.Button(frame_comp, text="📊 EJECUTAR COMPARATIVA COMPLETA", 
                                command=self.comparar_todos,
                                bg='#e94560', fg='white', font=("Arial", 12, "bold"), 
                                pady=10)
        btn_comparar.pack(pady=10)
        
        # Área de resultados
        text_frame = tk.Frame(frame_comp, bg='#16213e')
        text_frame.pack(fill=tk.BOTH, expand=True)
        
        scroll_texto = tk.Scrollbar(text_frame)
        self.text_comparativa = tk.Text(text_frame, yscrollcommand=scroll_texto.set,
                                        bg='#0f3460', fg='#00ff88', font=("Consolas", 10), wrap=tk.WORD)
        scroll_texto.config(command=self.text_comparativa.yview)
        
        self.text_comparativa.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scroll_texto.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.text_comparativa.tag_config("verde", foreground="#00ff88")
        self.text_comparativa.tag_config("amarillo", foreground="#ffd700")
        self.text_comparativa.tag_config("rojo", foreground="#ff6666")
        self.text_comparativa.tag_config("azul", foreground="#66b3ff")
    
    def _escribir(self, texto, tag=None, target="medir"):
        if target == "medir":
            self.text_medir.insert(tk.END, texto, tag)
            self.text_medir.see(tk.END)
        elif target == "comparativa":
            self.text_comparativa.insert(tk.END, texto, tag)
            self.text_comparativa.see(tk.END)
        self.update()
    
    def _bienvenida(self):
        self._escribir("="*65, "amarillo")
        self._escribir("📊 PROGRAMA DE PRUEBA - TUS LIBRERÍAS\n", "verde")
        self._escribir("="*65, "amarillo")
        self._escribir(f"\n✅ Algoritmos para medir tiempo: {len(ALGORITMOS_MEDIR)}\n", "azul")
        self._escribir(f"✅ Algoritmos para visualizar: {len(ALGORITMOS_VISUALES)}\n", "azul")
        self._escribir(f"✅ Lectores disponibles: {len(LECTORES)}\n", "azul")
        self._escribir("\n▶️ INSTRUCCIONES:\n")
        self._escribir("   1. Haz clic en 'Random' para generar datos\n")
        self._escribir("   2. Ve a la pestaña 'MEDIR TIEMPO' y selecciona un algoritmo\n")
        self._escribir("   3. Ve a 'VISUALIZACIÓN' para ver el proceso paso a paso\n")
        self._escribir("   4. Usa 'COMPARATIVA' para ranking de velocidades\n")
        self._escribir("="*65 + "\n\n", "amarillo")
    
    def actualizar_label(self):
        if self.datos:
            mostrar = str(self.datos[:10])
            if len(self.datos) > 10:
                mostrar += f"... (+{len(self.datos)-10})"
            self.label_datos.config(text=f"📊 {len(self.datos)} elementos: {mostrar}")
        else:
            self.label_datos.config(text="📊 Sin datos cargados")
    
    # ========== MÉTODOS DE CARGA ==========
    def cargar_txt(self):
        ruta = filedialog.askopenfilename(filetypes=[("Text", "*.txt")])
        if ruta and 'txt' in LECTORES:
            try:
                self.datos = LECTORES['txt'](ruta)
                self.actualizar_label()
                self._escribir(f"✅ TXT: {len(self.datos)} números\n", "verde")
            except Exception as e:
                messagebox.showerror("Error", str(e))
    
    def cargar_json(self):
        ruta = filedialog.askopenfilename(filetypes=[("JSON", "*.json")])
        if ruta and 'json' in LECTORES:
            try:
                self.datos = LECTORES['json'](ruta)
                self.actualizar_label()
                self._escribir(f"✅ JSON: {len(self.datos)} números\n", "verde")
            except Exception as e:
                messagebox.showerror("Error", str(e))
    
    def cargar_word(self):
        ruta = filedialog.askopenfilename(filetypes=[("Word", "*.docx")])
        if ruta and 'word' in LECTORES:
            try:
                self.datos = LECTORES['word'](ruta)
                self.actualizar_label()
                self._escribir(f"✅ Word: {len(self.datos)} números\n", "verde")
            except Exception as e:
                messagebox.showerror("Error", str(e))
    
    def cargar_excel(self):
        ruta = filedialog.askopenfilename(filetypes=[("Excel", "*.xlsx")])
        if ruta and 'excel' in LECTORES:
            try:
                self.datos = LECTORES['excel'](ruta)
                self.actualizar_label()
                self._escribir(f"✅ Excel: {len(self.datos)} números\n", "verde")
            except Exception as e:
                messagebox.showerror("Error", str(e))
    
    def generar_random(self):
        self.datos = [random.randint(1, 100) for _ in range(20)]
        self.actualizar_label()
        self._escribir(f"🎲 Random: {len(self.datos)} números\n", "amarillo")
        self._escribir(f"   {self.datos}\n\n")
    
    def usar_manual(self):
        try:
            texto = self.entry.get().replace(',', ' ')
            self.datos = list(map(int, texto.split()))
            self.actualizar_label()
            self._escribir(f"📝 Manual: {len(self.datos)} números\n", "amarillo")
            self._escribir(f"   {self.datos}\n\n")
        except:
            messagebox.showerror("Error", "Ingresa números válidos")
    
    # ========== EJECUCIÓN PARA MEDIR TIEMPO ==========
    def ejecutar_medir(self, nombre):
        if not self.datos:
            self._escribir(f"❌ {nombre}: No hay datos\n", "rojo")
            return
        
        func = ALGORITMOS_MEDIR[nombre]
        
        try:
            inicio = time.perf_counter()
            resultado = func(self.datos)
            tiempo = (time.perf_counter() - inicio) * 1000
            
            self._escribir(f"\n{'─'*55}\n", "azul")
            self._escribir(f"📊 {nombre}\n", "verde")
            self._escribir(f"   ⏱️ TIEMPO: {tiempo:.3f} ms\n", "amarillo")
            self._escribir(f"   📏 Elementos: {len(self.datos)}\n")
            self._escribir(f"   Original: {self.datos[:8]}...\n")
            self._escribir(f"   Ordenado: {resultado[:8]}...\n\n")
            
            self.label_status.config(text=f"✅ {nombre[:30]} completado en {tiempo:.2f} ms")
            
        except Exception as e:
            self._escribir(f"❌ {nombre}: {str(e)[:60]}\n", "rojo")
    
    # ========== EJECUCIÓN PARA VISUALIZAR ==========
    def ejecutar_visualizar(self, nombre):
        if not self.datos:
            messagebox.showerror("Error", "Primero carga o genera datos")
            return
        
        func = ALGORITMOS_VISUALES[nombre]
        
        # Importar la función de visualización de la librería interna
        try:
            from ordenamiento_interno_Libreria import iniciar_grafico, actualizar_grafico, cerrar_grafico
            import matplotlib.pyplot as plt
            import threading
            
            def visualizar():
                try:
                    generador = func(self.datos)
                    for datos_paso, mensaje, idx_actual, idx_comp in generador:
                        iniciar_grafico()
                        actualizar_grafico(datos_paso, mensaje, None, idx_actual, idx_comp)
                        time.sleep(0.3)
                    plt.show(block=True)
                except Exception as e:
                    messagebox.showerror("Error", str(e))
            
            thread = threading.Thread(target=visualizar, daemon=True)
            thread.start()
            
            self.label_status.config(text=f"🎬 Visualizando {nombre}...")
            
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo visualizar: {e}")
    
    # ========== ORDENAMIENTO EXTERNO ==========
    def ejecutar_externo(self):
        if not EXTERNO_FUNC:
            self._escribir("❌ Externo no disponible\n", "rojo", target="medir")
            return
        if not self.datos:
            self._escribir("❌ No hay datos\n", "rojo", target="medir")
            return
        
        temp = "temp_externo.txt"
        with open(temp, 'w') as f:
            f.write(" ".join(map(str, self.datos)))
        
        try:
            inicio = time.perf_counter()
            resultado = EXTERNO_FUNC(temp, tamaño_bloque=5, usar_colores=False)
            tiempo = (time.perf_counter() - inicio) * 1000
            
            self._escribir(f"\n{'─'*55}\n", "azul", target="medir")
            self._escribir(f"💾 ORDENAMIENTO EXTERNO POR MEZCLA\n", "verde", target="medir")
            self._escribir(f"   ⏱️ TIEMPO: {tiempo:.3f} ms\n", "amarillo", target="medir")
            self._escribir(f"   📏 Elementos: {len(self.datos)}\n", target="medir")
            self._escribir(f"   Ordenado: {resultado[:8]}...\n", target="medir")
            self._escribir(f"   💾 Archivo: ordenado_externo.txt\n\n", target="medir")
            
            self.label_status.config(text=f"✅ Externo completado en {tiempo:.2f} ms")
            
        except Exception as e:
            self._escribir(f"❌ Externo: {str(e)[:60]}\n", "rojo", target="medir")
        finally:
            if os.path.exists(temp):
                os.remove(temp)
    
    # ========== COMPARATIVA ==========
    def comparar_todos(self):
        if not self.datos:
            self._escribir("❌ No hay datos para comparar\n", "rojo", target="comparativa")
            return
        
        self.text_comparativa.delete(1.0, tk.END)
        
        self._escribir("="*65 + "\n", "amarillo", target="comparativa")
        self._escribir("📊 COMPARATIVA DE RENDIMIENTO\n", "verde", target="comparativa")
        self._escribir(f"📏 Elementos: {len(self.datos)}\n", target="comparativa")
        self._escribir("="*65 + "\n\n", "amarillo", target="comparativa")
        
        resultados = []
        
        for nombre, func in ALGORITMOS_MEDIR.items():
            self.label_status.config(text=f"🔄 Probando {nombre[:30]}...")
            self.update()
            
            try:
                inicio = time.perf_counter()
                func(self.datos)
                tiempo = (time.perf_counter() - inicio) * 1000
                resultados.append((nombre, tiempo))
                self._escribir(f"  {nombre:<35} → {tiempo:>8.3f} ms\n", target="comparativa")
            except Exception as e:
                self._escribir(f"  {nombre:<35} → ERROR\n", "rojo", target="comparativa")
        
        if EXTERNO_FUNC:
            temp = "temp_comp.txt"
            with open(temp, 'w') as f:
                f.write(" ".join(map(str, self.datos)))
            try:
                inicio = time.perf_counter()
                EXTERNO_FUNC(temp, tamaño_bloque=5, usar_colores=False)
                tiempo = (time.perf_counter() - inicio) * 1000
                resultados.append(("💾 Externo por Mezcla", tiempo))
                self._escribir(f"  {'💾 Externo por Mezcla':<35} → {tiempo:>8.3f} ms\n", target="comparativa")
            except:
                pass
            finally:
                if os.path.exists(temp):
                    os.remove(temp)
        
        resultados.sort(key=lambda x: x[1])
        
        self._escribir("\n" + "="*65 + "\n", "amarillo", target="comparativa")
        self._escribir("🏆 RANKING DE VELOCIDAD\n\n", "amarillo", target="comparativa")
        
        for i, (nombre, tiempo) in enumerate(resultados, 1):
            medalla = "🥇" if i == 1 else ("🥈" if i == 2 else ("🥉" if i == 3 else "  "))
            self._escribir(f"{medalla} {i:2}. {nombre:<35} {tiempo:.3f} ms\n", 
                          "verde" if i==1 else None, target="comparativa")
        
        self._escribir("\n" + "="*65 + "\n", "amarillo", target="comparativa")
        self.label_status.config(text="✅ Comparativa completada")

# ============================================
# MAIN
# ============================================

if __name__ == "__main__":
    print("=" * 60)
    print("📊 PROGRAMA DE PRUEBA - VERSIÓN CORREGIDA")
    print(f"   Algoritmos para medir: {len(ALGORITMOS_MEDIR)}")
    print(f"   Algoritmos para visualizar: {len(ALGORITMOS_VISUALES)}")
    print(f"   Lectores: {len(LECTORES)}")
    print("=" * 60)
    
    app = AppPruebaFinal()
    app.mainloop()