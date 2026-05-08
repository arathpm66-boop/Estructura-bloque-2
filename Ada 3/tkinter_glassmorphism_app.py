# 🔥 MODO DIOS: VISUALIZADOR DE ORDENAMIENTOS 🔥
import tkinter as tk
from tkinter import messagebox, filedialog
import random
import json
import matplotlib.pyplot as plt

# ══════════════════════════════════════════════════════
# CONFIG
# ══════════════════════════════════════════════════════
velocidad = 0.4

# ══════════════════════════════════════════════════════
# ALGORITMOS CON RESALTADO
# ══════════════════════════════════════════════════════

def intercalacion_steps(a, b):
    pasos = []
    colores = []
    resultado = []
    i = j = 0

    while i < len(a) and j < len(b):
        if a[i] < b[j]:
            resultado.append(a[i])
            i += 1
        else:
            resultado.append(b[j])
            j += 1

        pasos.append(resultado.copy())
        colores.append(["red" if k == len(resultado)-1 else "gray" for k in range(len(resultado))])

    resultado.extend(a[i:])
    resultado.extend(b[j:])
    pasos.append(resultado.copy())
    colores.append(["green"] * len(resultado))

    return pasos, colores


def mezcla_directa_steps(lista):
    pasos = []
    colores = []

    def merge_sort(arr):
        if len(arr) <= 1:
            return arr

        mid = len(arr)//2
        left = merge_sort(arr[:mid])
        right = merge_sort(arr[mid:])

        merged = []
        i = j = 0

        while i < len(left) and j < len(right):
            if left[i] < right[j]:
                merged.append(left[i]); i += 1
            else:
                merged.append(right[j]); j += 1

            pasos.append(merged.copy())
            colores.append(["red" if k == len(merged)-1 else "gray" for k in range(len(merged))])

        merged.extend(left[i:])
        merged.extend(right[j:])

        pasos.append(merged.copy())
        colores.append(["green"] * len(merged))

        return merged

    merge_sort(lista)
    return pasos, colores


def mezcla_equilibrada_steps(lista):
    return mezcla_directa_steps(lista)

# ══════════════════════════════════════════════════════
# GRAFICADOR PRO
# ══════════════════════════════════════════════════════

def graficar(pasos, colores, titulo):
    plt.ion()
    fig, ax = plt.subplots()

    for i, paso in enumerate(pasos):
        ax.clear()
        ax.set_title(f"{titulo} - Paso {i+1}")

        c = colores[i] if i < len(colores) else ["gray"] * len(paso)
        ax.bar(range(len(paso)), paso, color=c)

        ax.set_xticks(range(len(paso)))
        ax.set_xticklabels(paso)

        plt.pause(velocidad)

    plt.ioff()
    plt.show()

# ══════════════════════════════════════════════════════
# JSON
# ══════════════════════════════════════════════════════

def cargar_json(entry):
    file = filedialog.askopenfilename(filetypes=[("JSON", "*.json")])
    if not file:
        return
    try:
        with open(file, "r", encoding="utf-8") as f:
            data = json.load(f)
        nums = data.get("numeros", [])
        entry.delete(0, "end")
        entry.insert(0, ", ".join(map(str, nums)))
    except Exception as e:
        messagebox.showerror("Error", str(e))

# ══════════════════════════════════════════════════════
# APP
# ══════════════════════════════════════════════════════

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("🔥 MODO DIOS - Ordenamientos 🔥")
        self.geometry("850x500")
        self.configure(bg="#0F0F1A")
        self.build()

    def build(self):
        tk.Label(self, text="📂 Datos",
                 bg="#0F0F1A", fg="#A78BFA",
                 font=("Segoe UI", 16, "bold")).pack(pady=10)

        self.entry = tk.Entry(self, width=70)
        self.entry.pack(pady=10)

        frame = tk.Frame(self, bg="#0F0F1A")
        frame.pack()

        tk.Button(frame, text="JSON",
                  command=lambda: cargar_json(self.entry)).pack(side="left", padx=5)

        tk.Button(frame, text="Random",
                  command=self.random_data).pack(side="left", padx=5)

        tk.Button(frame, text="Intercalación",
                  command=self.run_intercalacion).pack(side="left", padx=5)

        tk.Button(frame, text="Mezcla Directa",
                  command=self.run_directa).pack(side="left", padx=5)

        tk.Button(frame, text="Mezcla Equilibrada",
                  command=self.run_equilibrada).pack(side="left", padx=5)

        tk.Button(frame, text="⚡ Más rápido",
                  command=self.mas_rapido).pack(side="left", padx=5)

        tk.Button(frame, text="🐢 Más lento",
                  command=self.mas_lento).pack(side="left", padx=5)

    def get_data(self):
        return [int(x.strip()) for x in self.entry.get().split(",") if x.strip()]

    def random_data(self):
        data = random.sample(range(1, 100), 10)
        self.entry.delete(0, "end")
        self.entry.insert(0, ", ".join(map(str, data)))

    def run_intercalacion(self):
        data = self.get_data()
        mitad = len(data)//2
        a = sorted(data[:mitad])
        b = sorted(data[mitad:])
        pasos, colores = intercalacion_steps(a, b)
        graficar(pasos, colores, "Intercalación")

    def run_directa(self):
        data = self.get_data()
        pasos, colores = mezcla_directa_steps(data)
        graficar(pasos, colores, "Mezcla Directa")

    def run_equilibrada(self):
        data = self.get_data()
        pasos, colores = mezcla_equilibrada_steps(data)
        graficar(pasos, colores, "Mezcla Equilibrada")

    def mas_rapido(self):
        global velocidad
        velocidad = max(0.1, velocidad - 0.1)

    def mas_lento(self):
        global velocidad
        velocidad += 0.1


if __name__ == "__main__":
    App().mainloop()
