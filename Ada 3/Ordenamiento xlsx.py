import tkinter as tk
from tkinter import filedialog, messagebox
import json
from docx import Document
import matplotlib.pyplot as plt
import pandas as pd
import random

plt.ion()

# =====================
# ESTILO (Glassmorphism básico)
# =====================
BG_COLOR = "#0f172a"
CARD_COLOR = "#1e293b"
BTN_COLOR = "#38bdf8"
TEXT_COLOR = "#e2e8f0"

# =====================
# LECTURA ARCHIVOS
# =====================

def leer_json(ruta):
    with open(ruta, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data["datos"]


def leer_txt(ruta):
    with open(ruta, 'r', encoding='utf-8') as f:
        return list(map(int, f.read().split()))


def leer_word(ruta):
    doc = Document(ruta)
    texto = ""
    for p in doc.paragraphs:
        texto += p.text + " "
    return list(map(int, texto.split()))


def leer_excel(ruta):
    xls = pd.ExcelFile(ruta)
    hojas = {}
    for hoja in xls.sheet_names:
        df = pd.read_excel(xls, sheet_name=hoja)
        datos = df.select_dtypes(include='number').values.flatten()
        datos = [int(x) for x in datos if not pd.isna(x)]
        if datos:
            hojas[hoja] = datos
    return hojas

# =====================
# GRAFICAR
# =====================

def graficar(datos, titulo):
    plt.clf()
    plt.bar(range(len(datos)), datos)
    plt.title(titulo)
    plt.pause(0.2)

# =====================
# ORDENAMIENTOS
# =====================

def intercalacion(datos):
    arr = datos.copy()
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        while j >= 0 and key < arr[j]:
            arr[j + 1] = arr[j]
            j -= 1
            graficar(arr, "Intercalación")
        arr[j + 1] = key


def mezcla_directa(datos):
    def merge_sort(arr):
        if len(arr) > 1:
            mid = len(arr)//2
            L = arr[:mid]
            R = arr[mid:]

            merge_sort(L)
            merge_sort(R)

            i = j = k = 0
            while i < len(L) and j < len(R):
                if L[i] < R[j]:
                    arr[k] = L[i]
                    i += 1
                else:
                    arr[k] = R[j]
                    j += 1
                k += 1
                graficar(arr, "Mezcla Directa")

    arr = datos.copy()
    merge_sort(arr)


def mezcla_equilibrada(datos):
    arr = sorted(datos)
    for i in range(len(arr)):
        graficar(arr, f"Paso {i+1}")

# =====================
# INTERFAZ
# =====================

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Ordenamientos Visuales PRO")
        self.root.geometry("500x500")
        self.root.configure(bg=BG_COLOR)

        self.datos = []
        self.hojas_excel = {}

        # Card principal
        frame = tk.Frame(root, bg=CARD_COLOR)
        frame.pack(padx=20, pady=20, fill="both", expand=True)

        tk.Label(frame, text="Ordenamientos Visuales", fg=TEXT_COLOR, bg=CARD_COLOR, font=("Arial", 16, "bold")).pack(pady=10)

        tk.Button(frame, text="📂 Cargar Archivo", bg=BTN_COLOR, command=self.cargar).pack(fill="x", pady=5)

        self.entry = tk.Entry(frame)
        self.entry.pack(fill="x", pady=5)

        tk.Button(frame, text="✍️ Usar datos manuales", bg=BTN_COLOR, command=self.usar_manual).pack(fill="x", pady=5)

        tk.Button(frame, text="🎲 Generar aleatorios", bg=BTN_COLOR, command=self.generar_random).pack(fill="x", pady=5)

        self.lista_hojas = tk.Listbox(frame)
        self.lista_hojas.pack(fill="x", pady=5)

        tk.Button(frame, text="📊 Usar hoja seleccionada", bg=BTN_COLOR, command=self.usar_hoja).pack(fill="x", pady=5)

        tk.Button(frame, text="Intercalación", bg=BTN_COLOR, command=self.run_intercalacion).pack(fill="x", pady=5)
        tk.Button(frame, text="Mezcla Directa", bg=BTN_COLOR, command=self.run_mezcla).pack(fill="x", pady=5)
        tk.Button(frame, text="Mezcla Equilibrada", bg=BTN_COLOR, command=self.run_equilibrada).pack(fill="x", pady=5)

    def usar_manual(self):
        try:
            self.datos = list(map(int, self.entry.get().split()))
            messagebox.showinfo("Datos", f"{self.datos}")
        except:
            messagebox.showerror("Error", "Datos inválidos")

    def generar_random(self):
        self.datos = [random.randint(1, 100) for _ in range(10)]
        messagebox.showinfo("Random", f"{self.datos}")

    def cargar(self):
        ruta = filedialog.askopenfilename(filetypes=[("Archivos", "*.json *.txt *.docx *.xlsx")])
        if not ruta:
            return

        try:
            if ruta.endswith(".json"):
                self.datos = leer_json(ruta)
            elif ruta.endswith(".txt"):
                self.datos = leer_txt(ruta)
            elif ruta.endswith(".docx"):
                self.datos = leer_word(ruta)
            elif ruta.endswith(".xlsx"):
                self.hojas_excel = leer_excel(ruta)
                self.lista_hojas.delete(0, tk.END)
                for hoja in self.hojas_excel:
                    self.lista_hojas.insert(tk.END, hoja)
                return

            messagebox.showinfo("Éxito", f"{self.datos}")

        except Exception as e:
            messagebox.showerror("Error", str(e))

    def usar_hoja(self):
        sel = self.lista_hojas.curselection()
        if sel:
            hoja = self.lista_hojas.get(sel)
            self.datos = self.hojas_excel[hoja]
            messagebox.showinfo("Hoja", f"{self.datos}")

    def validar(self):
        if not self.datos:
            messagebox.showwarning("Error", "Carga datos primero")
            return False
        return True

    def run_intercalacion(self):
        if self.validar():
            plt.figure()
            intercalacion(self.datos)
            plt.show()

    def run_mezcla(self):
        if self.validar():
            plt.figure()
            mezcla_directa(self.datos)
            plt.show()

    def run_equilibrada(self):
        if self.validar():
            plt.figure()
            mezcla_equilibrada(self.datos)
            plt.show()

# MAIN
if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()