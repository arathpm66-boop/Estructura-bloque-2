# ============================================
# 🔥 ORDENAMIENTOS PRO - VERSIÓN CORREGIDA 🔥
# SOLO UNA VENTANA DE GRÁFICO
# ============================================

import tkinter as tk
from tkinter import ttk, filedialog, messagebox, simpledialog
import random
import json
import os
import pandas as pd
from docx import Document
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import time

# Configuración global
velocidad = 0.4
fig = None  # Referencia global a la figura
ax = None   # Referencia global al eje

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
        raise ValueError("JSON debe contener una lista de números")

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
    raise ValueError("El Excel no contiene datos numéricos válidos")

# ============================================
# VISUALIZACIÓN - SOLO UNA VENTANA
# ============================================

def iniciar_grafico():
    """Inicializa la ventana de gráfico SOLO UNA VEZ"""
    global fig, ax
    if fig is None or not plt.fignum_exists(fig.number):
        plt.ion()
        fig, ax = plt.subplots(figsize=(12, 6))
        fig.canvas.manager.set_window_title('Visualizador de Ordenamientos')
        ax.set_title("Ordenamiento en progreso...")
        ax.set_xlabel("Posición")
        ax.set_ylabel("Valor")
    return fig, ax

def actualizar_grafico(datos, titulo, colores=None):
    """Actualiza el gráfico en la misma ventana"""
    global fig, ax
    
    # Asegurar que existe la ventana
    if fig is None or not plt.fignum_exists(fig.number):
        fig, ax = iniciar_grafico()
    
    ax.clear()
    
    if colores is None:
        colores = ['steelblue'] * len(datos)
    
    barras = ax.bar(range(len(datos)), datos, color=colores)
    ax.set_title(titulo, fontsize=14, fontweight='bold')
    ax.set_xlabel("Posición", fontsize=12)
    ax.set_ylabel("Valor", fontsize=12)
    
    # Mostrar valores encima de las barras
    for i, barra in enumerate(barras):
        altura = barra.get_height()
        ax.text(barra.get_x() + barra.get_width()/2., altura,
                f'{int(altura)}', ha='center', va='bottom', fontsize=8)
    
    plt.tight_layout()
    plt.draw()
    plt.pause(velocidad)

def cerrar_grafico():
    """Cierra la ventana de gráfico"""
    global fig
    if fig is not None:
        plt.close(fig)
        fig = None

# ============================================
# ORDENAMIENTOS INTERNOS
# ============================================

def intercalacion(datos, usar_colores=True):
    """Ordenamiento por Inserción (Intercalación)"""
    arr = datos.copy()
    
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        
        while j >= 0 and key < arr[j]:
            arr[j + 1] = arr[j]
            j -= 1
            
            if usar_colores:
                colores = ['lightcoral' if x == j+1 or x == i else 'steelblue' for x in range(len(arr))]
                actualizar_grafico(arr, f"Inserción - Pasando elemento {key}", colores)
            else:
                actualizar_grafico(arr, f"Inserción - Paso {i}")
        
        arr[j + 1] = key
        
        if usar_colores:
            colores = ['gold' if x == j+1 else 'steelblue' for x in range(len(arr))]
            actualizar_grafico(arr, f"Inserción - Insertando {key}", colores)
    
    colores = ['forestgreen'] * len(arr)
    actualizar_grafico(arr, "✅ Inserción Completado", colores)
    return arr

def mezcla_directa(datos, usar_colores=True):
    """Mezcla Directa (Merge Sort)"""
    arr = datos.copy()
    
    def merge_sort(arr_local):
        if len(arr_local) <= 1:
            return arr_local
        
        mid = len(arr_local) // 2
        left = merge_sort(arr_local[:mid])
        right = merge_sort(arr_local[mid:])
        
        # Mezclar
        resultado = []
        i = j = 0
        
        while i < len(left) and j < len(right):
            if left[i] <= right[j]:
                resultado.append(left[i])
                i += 1
            else:
                resultado.append(right[j])
                j += 1
            
            if usar_colores:
                colores = ['orange' if x == len(resultado)-1 else 'steelblue' for x in range(len(resultado))]
                actualizar_grafico(resultado, "Mezcla Directa - Mezclando", colores)
            else:
                actualizar_grafico(resultado, "Mezcla Directa")
        
        resultado.extend(left[i:])
        resultado.extend(right[j:])
        
        return resultado
    
    resultado_final = merge_sort(arr)
    colores = ['forestgreen'] * len(resultado_final)
    actualizar_grafico(resultado_final, "✅ Mezcla Directa Completado", colores)
    return resultado_final

def mezcla_equilibrada(datos, usar_colores=True):
    """Mezcla Equilibrada (versión iterativa)"""
    arr = datos.copy()
    ancho = 1
    paso = 0
    
    while ancho < len(arr):
        for inicio in range(0, len(arr), 2 * ancho):
            medio = min(inicio + ancho, len(arr))
            fin = min(inicio + 2 * ancho, len(arr))
            
            if medio < fin:
                izquierda = arr[inicio:medio]
                derecha = arr[medio:fin]
                
                i = j = 0
                k = inicio
                
                while i < len(izquierda) and j < len(derecha):
                    if izquierda[i] <= derecha[j]:
                        arr[k] = izquierda[i]
                        i += 1
                    else:
                        arr[k] = derecha[j]
                        j += 1
                    k += 1
                
                while i < len(izquierda):
                    arr[k] = izquierda[i]
                    i += 1
                    k += 1
                
                while j < len(derecha):
                    arr[k] = derecha[j]
                    j += 1
                    k += 1
        
        paso += 1
        actualizar_grafico(arr, f"Mezcla Equilibrada - Fase {paso}")
        ancho *= 2
    
    actualizar_grafico(arr, "✅ Mezcla Equilibrada Completado")
    return arr

# ============================================
# ORDENAMIENTOS EXTERNOS
# ============================================

def ordenamiento_externo_mezcla(archivo_entrada, tamaño_bloque=5, usar_colores=True):
    """Ordenamiento Externo por Mezcla - PARA DATOS QUE NO CABEN EN RAM"""
    
    print("📂 Iniciando Ordenamiento Externo...")
    
    # Leer archivo
    with open(archivo_entrada, 'r') as f:
        datos_originales = list(map(int, f.read().split()))
    
    print(f"📊 Total de datos: {len(datos_originales)}")
    print(f"🗂️ Tamaño de bloque: {tamaño_bloque}")
    
    actualizar_grafico(datos_originales, f"Datos originales ({len(datos_originales)} elementos)")
    
    # Dividir en bloques ordenados
    bloques = []
    for i in range(0, len(datos_originales), tamaño_bloque):
        bloque = sorted(datos_originales[i:i + tamaño_bloque])
        nombre_bloque = f"temp_bloque_{i//tamaño_bloque}.txt"
        with open(nombre_bloque, 'w') as temp:
            temp.write(" ".join(map(str, bloque)))
        bloques.append(nombre_bloque)
    
    # Mezclar todos los bloques
    listas = []
    for bloque in bloques:
        with open(bloque, 'r') as f:
            listas.append(list(map(int, f.read().split())))
    
    indices = [0] * len(listas)
    resultado = []
    
    while True:
        # Encontrar el mínimo
        min_valor = float('inf')
        min_idx = -1
        
        for i in range(len(listas)):
            if indices[i] < len(listas[i]) and listas[i][indices[i]] < min_valor:
                min_valor = listas[i][indices[i]]
                min_idx = i
        
        if min_idx == -1:
            break
        
        resultado.append(min_valor)
        indices[min_idx] += 1
        
        # Actualizar gráfico cada cierto número de elementos
        if len(resultado) % max(1, len(datos_originales)//20) == 0 or len(resultado) == len(datos_originales):
            actualizar_grafico(resultado, f"Mezcla Externa - {len(resultado)}/{len(datos_originales)}")
    
    # Guardar resultado
    with open("ordenado_externo.txt", 'w') as out:
        out.write(" ".join(map(str, resultado)))
    
    # Limpiar archivos temporales
    for bloque in bloques:
        if os.path.exists(bloque):
            os.remove(bloque)
    
    actualizar_grafico(resultado, "✅ Ordenamiento Externo Completado", ['forestgreen'] * len(resultado))
    return resultado

# ============================================
# INTERFAZ MODERNA
# ============================================

class AppModerno(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("🔥 ORDENAMIENTOS PRO - Con Métodos Externos 🔥")
        self.geometry("900x650")
        self.configure(bg="#0F0F1A")
        
        # Variables
        self.datos = []
        self.velocidad_var = tk.DoubleVar(value=0.4)
        self.color_var = tk.BooleanVar(value=True)
        
        self.build_ui()
        
        # Cerrar gráfico al salir
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
    
    def on_closing(self):
        cerrar_grafico()
        self.destroy()
    
    def build_ui(self):
        # Título
        titulo = tk.Label(self, text="📊 SISTEMA AVANZADO DE ORDENAMIENTOS", 
                         bg="#0F0F1A", fg="#A78BFA", font=("Segoe UI", 18, "bold"))
        titulo.pack(pady=15)
        
        # Frame de datos
        frame_datos = tk.LabelFrame(self, text="📁 Datos", bg="#1A1A2E", fg="white", 
                                   font=("Segoe UI", 12, "bold"), padx=10, pady=10)
        frame_datos.pack(fill=tk.X, padx=20, pady=10)
        
        # Entrada manual
        tk.Label(frame_datos, text="Ingresa números (separados por coma o espacio):", 
                bg="#1A1A2E", fg="white").pack(anchor=tk.W)
        self.entry = tk.Entry(frame_datos, width=80, font=("Consolas", 10))
        self.entry.pack(pady=5)
        
        # Botones de carga
        frame_botones = tk.Frame(frame_datos, bg="#1A1A2E")
        frame_botones.pack(pady=5)
        
        botones = [
            ("📄 TXT", self.cargar_txt),
            ("📦 JSON", self.cargar_json),
            ("📝 Word", self.cargar_word),
            ("📊 Excel", self.cargar_excel),
            ("🎲 Random", self.generar_random),
            ("✅ Usar Manual", self.usar_manual)
        ]
        
        for texto, comando in botones:
            tk.Button(frame_botones, text=texto, command=comando, 
                     bg="#2D2D44", fg="white", padx=15, pady=3).pack(side=tk.LEFT, padx=5)
        
        # Mostrar datos actuales
        self.label_datos = tk.Label(frame_datos, text="📊 Sin datos cargados", 
                                   bg="#1A1A2E", fg="#FFD700", font=("Consolas", 10))
        self.label_datos.pack(pady=5)
        
        # Frame de controles
        frame_controles = tk.LabelFrame(self, text="⚙️ Controles", bg="#1A1A2E", fg="white",
                                       font=("Segoe UI", 12, "bold"), padx=10, pady=10)
        frame_controles.pack(fill=tk.X, padx=20, pady=10)
        
        # Velocidad
        tk.Label(frame_controles, text="Velocidad:", bg="#1A1A2E", fg="white").pack(side=tk.LEFT, padx=5)
        velocidad_scale = tk.Scale(frame_controles, from_=0.05, to=1.0, resolution=0.05,
                                  orient=tk.HORIZONTAL, variable=self.velocidad_var,
                                  length=200, bg="#1A1A2E", fg="white",
                                  command=self.cambiar_velocidad)
        velocidad_scale.pack(side=tk.LEFT, padx=5)
        
        # Checkbox colores
        tk.Checkbutton(frame_controles, text="Visualización con colores", 
                      variable=self.color_var, bg="#1A1A2E", fg="white",
                      selectcolor="#2D2D44").pack(side=tk.LEFT, padx=20)
        
        # Frame de algoritmos
        frame_alg = tk.LabelFrame(self, text="🧠 Algoritmos de Ordenamiento", bg="#1A1A2E", fg="white",
                                 font=("Segoe UI", 12, "bold"), padx=10, pady=10)
        frame_alg.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # Algoritmos internos
        tk.Label(frame_alg, text="📌 INTERNOS (En memoria RAM)", 
                bg="#1A1A2E", fg="#A78BFA", font=("Segoe UI", 11, "bold")).pack(pady=5)
        
        frame_internos = tk.Frame(frame_alg, bg="#1A1A2E")
        frame_internos.pack(pady=5)
        
        internos = [
            ("🔹 Inserción (Intercalación)", self.run_insercion),
            ("🔸 Mezcla Directa (Merge Sort)", self.run_mezcla_directa),
            ("🔹 Mezcla Equilibrada", self.run_mezcla_equilibrada)
        ]
        
        for texto, comando in internos:
            tk.Button(frame_internos, text=texto, command=comando,
                     bg="#3D3D5C", fg="white", width=25, height=2).pack(pady=3)
        
        # Algoritmos externos
        tk.Label(frame_alg, text="💾 EXTERNOS (Por archivos)", 
                bg="#1A1A2E", fg="#FF6B6B", font=("Segoe UI", 11, "bold")).pack(pady=10)
        
        frame_externos = tk.Frame(frame_alg, bg="#1A1A2E")
        frame_externos.pack(pady=5)
        
        tk.Button(frame_externos, text="💿 Ordenamiento Externo por Mezcla", 
                 command=self.run_externo, bg="#5C3D6E", fg="white", 
                 width=30, height=2, font=("Segoe UI", 10, "bold")).pack(pady=3)
        
        # Botón limpiar
        tk.Button(frame_alg, text="🗑️ Limpiar Archivos Temporales", 
                 command=self.limpiar_temp, bg="#E74C3C", fg="white",
                 width=30, height=1).pack(pady=10)
        
        # Estado
        self.label_status = tk.Label(self, text="✅ Sistema listo | Solo UNA ventana de gráfico", 
                                    bg="#0F0F1A", fg="#2ECC71", font=("Segoe UI", 10))
        self.label_status.pack(pady=10)
    
    def cambiar_velocidad(self, val):
        global velocidad
        velocidad = self.velocidad_var.get()
    
    def actualizar_datos_ui(self):
        if self.datos:
            mostrar = str(self.datos[:20])
            if len(self.datos) > 20:
                mostrar += f"... (+{len(self.datos)-20} más)"
            self.label_datos.config(text=f"📊 {len(self.datos)} datos: {mostrar}")
        else:
            self.label_datos.config(text="📊 Sin datos cargados")
    
    # Métodos de carga
    def cargar_txt(self):
        ruta = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
        if ruta:
            try:
                self.datos = leer_txt(ruta)
                self.actualizar_datos_ui()
                messagebox.showinfo("Éxito", f"Cargados {len(self.datos)} números")
            except Exception as e:
                messagebox.showerror("Error", str(e))
    
    def cargar_json(self):
        ruta = filedialog.askopenfilename(filetypes=[("JSON files", "*.json")])
        if ruta:
            try:
                self.datos = leer_json(ruta)
                self.actualizar_datos_ui()
                messagebox.showinfo("Éxito", f"Cargados {len(self.datos)} números")
            except Exception as e:
                messagebox.showerror("Error", str(e))
    
    def cargar_word(self):
        ruta = filedialog.askopenfilename(filetypes=[("Word files", "*.docx")])
        if ruta:
            try:
                self.datos = leer_word(ruta)
                self.actualizar_datos_ui()
                messagebox.showinfo("Éxito", f"Cargados {len(self.datos)} números")
            except Exception as e:
                messagebox.showerror("Error", str(e))
    
    def cargar_excel(self):
        ruta = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx")])
        if ruta:
            try:
                self.datos = leer_excel(ruta)
                self.actualizar_datos_ui()
                messagebox.showinfo("Éxito", f"Cargados {len(self.datos)} números")
            except Exception as e:
                messagebox.showerror("Error", str(e))
    
    def generar_random(self):
        cantidad = 15
        self.datos = [random.randint(1, 100) for _ in range(cantidad)]
        self.actualizar_datos_ui()
        messagebox.showinfo("Random", f"Generados {cantidad} números aleatorios:\n{self.datos}")
    
    def usar_manual(self):
        try:
            texto = self.entry.get()
            texto = texto.replace(',', ' ')
            self.datos = list(map(int, texto.split()))
            self.actualizar_datos_ui()
            messagebox.showinfo("Manual", f"Datos cargados: {self.datos[:20]}")
        except Exception as e:
            messagebox.showerror("Error", "Ingresa números válidos separados por comas o espacios")
    
    # Métodos de ordenamiento
    def run_insercion(self):
        if not self.datos:
            messagebox.showerror("Error", "Primero carga o genera datos")
            return
        iniciar_grafico()
        intercalacion(self.datos, usar_colores=self.color_var.get())
        plt.show(block=True)  # Esperar a que el usuario cierre
    
    def run_mezcla_directa(self):
        if not self.datos:
            messagebox.showerror("Error", "Primero carga o genera datos")
            return
        iniciar_grafico()
        mezcla_directa(self.datos, usar_colores=self.color_var.get())
        plt.show(block=True)
    
    def run_mezcla_equilibrada(self):
        if not self.datos:
            messagebox.showerror("Error", "Primero carga o genera datos")
            return
        iniciar_grafico()
        mezcla_equilibrada(self.datos, usar_colores=self.color_var.get())
        plt.show(block=True)
    
    def run_externo(self):
        if not self.datos:
            messagebox.showerror("Error", "Primero carga o genera datos")
            return
        
        temp_file = "temp_entrada_externo.txt"
        with open(temp_file, 'w') as f:
            f.write(" ".join(map(str, self.datos)))
        
        tamaño = 5
        try:
            respuesta = simpledialog.askinteger("Tamaño de bloque", 
                                               "¿Cuántos números por bloque? (recomendado: 3-10)",
                                               initialvalue=5, minvalue=2, maxvalue=20)
            if respuesta:
                tamaño = respuesta
        except:
            pass
        
        try:
            iniciar_grafico()
            resultado = ordenamiento_externo_mezcla(temp_file, tamaño, usar_colores=self.color_var.get())
            plt.show(block=True)
            messagebox.showinfo("Completado", 
                               f"✅ Ordenamiento externo finalizado\n"
                               f"📁 Resultado guardado en 'ordenado_externo.txt'\n"
                               f"📊 Primeros 20: {resultado[:20]}")
            self.label_status.config(text="✅ Ordenamiento externo completado")
        except Exception as e:
            messagebox.showerror("Error", str(e))
        finally:
            if os.path.exists(temp_file):
                os.remove(temp_file)
    
    def limpiar_temp(self):
        cont = 0
        for archivo in os.listdir('.'):
            if archivo.startswith('temp_bloque_') or archivo == 'ordenado_externo.txt':
                try:
                    os.remove(archivo)
                    cont += 1
                except:
                    pass
        messagebox.showinfo("Limpieza", f"Se eliminaron {cont} archivos temporales")

# ============================================
# MAIN
# ============================================

if __name__ == "__main__":
    print("=" * 50)
    print("🔥 ORDENAMIENTOS PRO - VERSIÓN CORREGIDA")
    print("✅ SOLO UNA ventana de gráfico se abre")
    print("✅ Incluye ordenamiento externo")
    print("=" * 50)
    
    app = AppModerno()
    app.mainloop()