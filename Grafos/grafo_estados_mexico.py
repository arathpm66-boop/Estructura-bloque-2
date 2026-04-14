"""
=============================================================================
GRAFO DE ESTADOS DE LA REPÚBLICA MEXICANA
=============================================================================
Descripción: Programa que modela un grafo ponderado de 7 estados mexicanos
             con sus conexiones y costos de traslado (en kilómetros).
             Implementa recorridos hamiltonianos y con repetición de nodos.

Autor: Ejercicio académico de Teoría de Grafos
Lenguaje: Python 3.x
Librerías: networkx, matplotlib
=============================================================================
"""

import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from itertools import permutations


# =============================================================================
# 1. DEFINICIÓN DEL GRAFO
# =============================================================================

def crear_grafo():
    """
    Crea y retorna un grafo ponderado no dirigido con 7 estados mexicanos.
    
    Los estados seleccionados forman una región conectada del centro-sur
    de México. Los pesos representan distancias aproximadas en kilómetros
    por carretera entre capitales de estado.
    
    Retorna:
        G (nx.Graph): Grafo no dirigido con nodos (estados) y aristas (rutas).
    """
    G = nx.Graph()

    # --- Nodos: 7 estados de la República Mexicana ---
    estados = [
        "Ciudad de México",  # CDMX  (nodo 0)
        "Puebla",            # PUE   (nodo 1)
        "Hidalgo",           # HGO   (nodo 2)
        "Morelos",           # MOR   (nodo 3)
        "Tlaxcala",          # TLAX  (nodo 4)
        "Estado de México",  # MEX   (nodo 5)
        "Guerrero",          # GRO   (nodo 6)
    ]
    G.add_nodes_from(estados)

    # --- Aristas: conexiones directas con peso (km aprox. por carretera) ---
    aristas = [
        ("Ciudad de México", "Puebla",           130),
        ("Ciudad de México", "Hidalgo",          100),
        ("Ciudad de México", "Morelos",           90),
        ("Ciudad de México", "Estado de México",  60),
        ("Puebla",           "Tlaxcala",          30),
        ("Puebla",           "Morelos",           180),
        ("Puebla",           "Hidalgo",           200),
        ("Hidalgo",          "Estado de México",  110),
        ("Morelos",          "Guerrero",          200),
        ("Estado de México", "Guerrero",          260),
        ("Tlaxcala",         "Hidalgo",           120),
    ]
    G.add_weighted_edges_from(aristas)

    return G


# =============================================================================
# 2. MOSTRAR LISTA DE ADYACENCIA
# =============================================================================

def mostrar_adyacencia(G):
    """
    Imprime en consola la lista de adyacencia del grafo,
    mostrando cada estado y sus vecinos directos con sus costos.

    Parámetros:
        G (nx.Graph): Grafo a analizar.
    """
    print("=" * 60)
    print("   LISTA DE ESTADOS Y SUS CONEXIONES DIRECTAS")
    print("=" * 60)
    for estado in G.nodes():
        vecinos = G[estado]
        conexiones = ", ".join(
            f"{v} ({d['weight']} km)" for v, d in vecinos.items()
        )
        print(f"  {estado:22} → {conexiones}")
    print("=" * 60)
    print(f"  Total de estados  : {G.number_of_nodes()}")
    print(f"  Total de conexiones: {G.number_of_edges()}")
    print("=" * 60)
    print()


# =============================================================================
# 3. RECORRIDO A — CAMINO HAMILTONIANO (sin repetir nodos)
# =============================================================================

def costo_camino(G, camino):
    """
    Calcula el costo total de un camino dado en el grafo.

    Parámetros:
        G (nx.Graph): Grafo ponderado.
        camino (list): Lista ordenada de nodos que forman el camino.

    Retorna:
        int | float | None: Costo total si el camino es válido, None si
                            alguna arista del camino no existe en el grafo.
    """
    costo = 0
    for i in range(len(camino) - 1):
        u, v = camino[i], camino[i + 1]
        if G.has_edge(u, v):
            costo += G[u][v]['weight']
        else:
            return None  # Arista inexistente → camino inválido
    return costo


def encontrar_camino_hamiltoniano(G):
    """
    Busca el camino hamiltoniano de menor costo usando fuerza bruta.
    Un camino hamiltoniano visita cada nodo exactamente una vez.

    Parámetros:
        G (nx.Graph): Grafo ponderado.

    Retorna:
        tuple: (mejor_camino, mejor_costo) o (None, None) si no existe.
    """
    nodos = list(G.nodes())
    mejor_camino = None
    mejor_costo = float('inf')

    # Probar todas las permutaciones posibles de nodos
    for permutacion in permutations(nodos):
        costo = costo_camino(G, list(permutacion))
        if costo is not None and costo < mejor_costo:
            mejor_costo = costo
            mejor_camino = list(permutacion)

    return mejor_camino, mejor_costo


def mostrar_recorrido_a(G):
    """
    Ejecuta y muestra el resultado del Recorrido A (camino hamiltoniano).

    Parámetros:
        G (nx.Graph): Grafo ponderado.

    Retorna:
        list: Aristas del camino hamiltoniano encontrado (para visualización).
    """
    print("=" * 60)
    print("   RECORRIDO A — CAMINO HAMILTONIANO (sin repetir estados)")
    print("=" * 60)

    camino, costo = encontrar_camino_hamiltoniano(G)

    if camino:
        print("  Ruta seguida:")
        for i, estado in enumerate(camino):
            if i < len(camino) - 1:
                peso = G[camino[i]][camino[i + 1]]['weight']
                print(f"    {i + 1}. {estado:22} ──({peso} km)──►")
            else:
                print(f"    {i + 1}. {estado}")
        print(f"\n  ✔ Costo total acumulado: {costo} km")

        # Retornar aristas del camino para resaltarlas en la visualización
        aristas_camino = [(camino[i], camino[i + 1]) for i in range(len(camino) - 1)]
    else:
        print("  ✘ No existe un camino hamiltoniano en este grafo.")
        aristas_camino = []

    print("=" * 60)
    print()
    return aristas_camino


# =============================================================================
# 4. RECORRIDO B — CON REPETICIÓN DE NODOS (BFS de cobertura mínima)
# =============================================================================

def recorrido_con_repeticion(G, inicio):
    """
    Realiza un recorrido que visita los 7 estados partiendo desde un nodo
    inicial, permitiendo repetir nodos cuando no hay camino directo.

    Estrategia: Greedy — desde el nodo actual, ir siempre al vecino no
    visitado más cercano. Si todos los vecinos ya fueron visitados,
    usar el camino más corto de Dijkstra hacia el nodo no visitado más
    cercano (lo que puede implicar repetir nodos intermedios).

    Parámetros:
        G (nx.Graph): Grafo ponderado.
        inicio (str): Nodo desde donde comienza el recorrido.

    Retorna:
        tuple: (camino_completo, costo_total)
    """
    visitados = set()
    camino_completo = [inicio]
    costo_total = 0
    nodo_actual = inicio
    visitados.add(inicio)

    todos_los_nodos = set(G.nodes())

    while visitados != todos_los_nodos:
        nodos_sin_visitar = todos_los_nodos - visitados

        # Buscar el nodo sin visitar más cercano usando Dijkstra
        mejor_destino = None
        mejor_costo_local = float('inf')
        mejor_subcamino = []

        for destino in nodos_sin_visitar:
            try:
                # Dijkstra retorna el camino más corto (puede repetir nodos)
                subcamino = nx.dijkstra_path(G, nodo_actual, destino, weight='weight')
                costo_local = nx.dijkstra_path_length(G, nodo_actual, destino, weight='weight')
                if costo_local < mejor_costo_local:
                    mejor_costo_local = costo_local
                    mejor_destino = destino
                    mejor_subcamino = subcamino
            except nx.NetworkXNoPath:
                continue

        if mejor_destino is None:
            # No hay camino hacia ningún nodo sin visitar (grafo desconectado)
            break

        # Agregar el subcamino (sin repetir el nodo de partida ya incluido)
        camino_completo.extend(mejor_subcamino[1:])
        costo_total += mejor_costo_local
        visitados.add(mejor_destino)
        nodo_actual = mejor_destino

    return camino_completo, costo_total


def mostrar_recorrido_b(G, inicio="Ciudad de México"):
    """
    Ejecuta y muestra el resultado del Recorrido B (con repetición permitida).

    Parámetros:
        G (nx.Graph): Grafo ponderado.
        inicio (str): Estado desde el que comienza el recorrido.

    Retorna:
        list: Aristas del recorrido para resaltarlas en la visualización.
    """
    print("=" * 60)
    print("   RECORRIDO B — CON REPETICIÓN DE NODOS PERMITIDA")
    print(f"   Inicio: {inicio}")
    print("=" * 60)

    camino, costo = recorrido_con_repeticion(G, inicio)

    print("  Ruta seguida (puede incluir repeticiones):")
    for i, estado in enumerate(camino):
        if i < len(camino) - 1:
            peso = G[camino[i]][camino[i + 1]]['weight']
            repetido = " ⟳" if camino.count(estado) > 1 else ""
            print(f"    {i + 1}. {estado:22}{repetido} ──({peso} km)──►")
        else:
            repetido = " ⟳" if camino.count(estado) > 1 else ""
            print(f"    {i + 1}. {estado}{repetido}")

    # Contar estados únicos visitados
    estados_visitados = set(camino)
    print(f"\n  Estados visitados ({len(estados_visitados)}/7): "
          f"{', '.join(sorted(estados_visitados))}")
    print(f"  ✔ Costo total acumulado: {costo} km")
    print("  (⟳ = nodo visitado más de una vez)")
    print("=" * 60)
    print()

    # Aristas para visualización
    aristas_camino = [(camino[i], camino[i + 1]) for i in range(len(camino) - 1)]
    return aristas_camino


# =============================================================================
# 5. VISUALIZACIÓN DEL GRAFO
# =============================================================================

def visualizar_grafo(G, aristas_hamilton, aristas_repeticion):
    """
    Dibuja el grafo completo y resalta los dos recorridos en subgráficos
    separados usando matplotlib y networkx.

    Parámetros:
        G (nx.Graph): Grafo ponderado.
        aristas_hamilton (list): Aristas del camino hamiltoniano.
        aristas_repeticion (list): Aristas del recorrido con repetición.
    """
    # Posiciones manuales aproximadas para reflejar la geografía real
    posiciones = {
        "Ciudad de México":  (0.50, 0.55),
        "Estado de México":  (0.30, 0.65),
        "Hidalgo":           (0.55, 0.80),
        "Tlaxcala":          (0.72, 0.70),
        "Puebla":            (0.75, 0.50),
        "Morelos":           (0.50, 0.35),
        "Guerrero":          (0.30, 0.18),
    }

    pesos_aristas = nx.get_edge_attributes(G, 'weight')

    # Paleta de colores con estética mexicana
    COLOR_FONDO      = "#1a1a2e"
    COLOR_NODO       = "#e94560"
    COLOR_NODO_BORDE = "#f5a623"
    COLOR_ARISTA     = "#4a4a6a"
    COLOR_HAMILTON   = "#00d4aa"
    COLOR_REPETICION = "#f5a623"
    COLOR_TEXTO      = "#ffffff"
    COLOR_PESO       = "#c8c8e8"

    fig, axes = plt.subplots(1, 3, figsize=(20, 7))
    fig.patch.set_facecolor(COLOR_FONDO)
    fig.suptitle(
        "Grafo de Estados de la República Mexicana",
        fontsize=18, fontweight='bold', color=COLOR_TEXTO, y=1.01
    )

    titulos = [
        "Grafo Completo\n(todas las conexiones)",
        "Recorrido A — Hamiltoniano\n(sin repetir estados)",
        "Recorrido B — Con Repetición\n(permitiendo revisitar estados)",
    ]
    colores_highlight = [None, COLOR_HAMILTON, COLOR_REPETICION]
    aristas_highlight = [[], aristas_hamilton, aristas_repeticion]

    for ax, titulo, color_h, aristas_h in zip(
            axes, titulos, colores_highlight, aristas_highlight):

        ax.set_facecolor(COLOR_FONDO)
        ax.set_title(titulo, color=COLOR_TEXTO, fontsize=11, fontweight='bold', pad=10)
        ax.axis('off')

        # Determinar color de cada arista
        if aristas_h:
            aristas_h_set = set(map(frozenset, aristas_h))
            colores = [
                color_h if frozenset([u, v]) in aristas_h_set else COLOR_ARISTA
                for u, v in G.edges()
            ]
            anchos = [
                3.5 if frozenset([u, v]) in aristas_h_set else 1.0
                for u, v in G.edges()
            ]
        else:
            colores = [COLOR_ARISTA] * G.number_of_edges()
            anchos  = [1.5] * G.number_of_edges()

        # Dibujar aristas
        nx.draw_networkx_edges(
            G, posiciones, ax=ax,
            edge_color=colores,
            width=anchos,
            alpha=0.85,
        )

        # Dibujar nodos
        nx.draw_networkx_nodes(
            G, posiciones, ax=ax,
            node_color=COLOR_NODO,
            node_size=900,
            edgecolors=COLOR_NODO_BORDE,
            linewidths=2.5,
        )

        # Etiquetas de nodos (nombres abreviados para legibilidad)
        etiquetas = {
            "Ciudad de México": "CDMX",
            "Estado de México": "Edo. Méx.",
            "Hidalgo":          "Hidalgo",
            "Tlaxcala":         "Tlaxcala",
            "Puebla":           "Puebla",
            "Morelos":          "Morelos",
            "Guerrero":         "Guerrero",
        }
        nx.draw_networkx_labels(
            G, posiciones, labels=etiquetas, ax=ax,
            font_size=8, font_color=COLOR_TEXTO, font_weight='bold'
        )

        # Etiquetas de pesos en las aristas
        nx.draw_networkx_edge_labels(
            G, posiciones, edge_labels=pesos_aristas, ax=ax,
            font_size=7, font_color=COLOR_PESO,
            bbox=dict(boxstyle='round,pad=0.2', fc=COLOR_FONDO, alpha=0.7, ec='none'),
            label_pos=0.5,
        )

    # Leyenda global
    leyenda = [
        mpatches.Patch(color=COLOR_HAMILTON,   label="Recorrido A (Hamiltoniano)"),
        mpatches.Patch(color=COLOR_REPETICION, label="Recorrido B (Con repetición)"),
        mpatches.Patch(color=COLOR_NODO,       label="Estado (nodo)"),
        mpatches.Patch(color=COLOR_ARISTA,     label="Conexión (arista)"),
    ]
    fig.legend(
        handles=leyenda,
        loc='lower center', ncol=4,
        fontsize=9, facecolor=COLOR_FONDO,
        labelcolor=COLOR_TEXTO,
        edgecolor=COLOR_NODO_BORDE,
        framealpha=0.8,
        bbox_to_anchor=(0.5, -0.04),
    )

    plt.tight_layout()
    # Guardar en la misma carpeta donde se ejecuta el script
    import os
    carpeta = os.path.dirname(os.path.abspath(__file__))
    ruta_imagen = os.path.join(carpeta, "grafo_mexico.png")
    plt.savefig(ruta_imagen, dpi=150, bbox_inches='tight',
                facecolor=COLOR_FONDO, edgecolor='none')
    print(f"  ✔ Visualización guardada en: {ruta_imagen}")
    plt.close()


# =============================================================================
# 6. PROGRAMA PRINCIPAL
# =============================================================================

def main():
    """
    Función principal que orquesta la ejecución del programa:
    1. Crea el grafo
    2. Muestra la lista de adyacencia
    3. Ejecuta y muestra el Recorrido A (hamiltoniano)
    4. Ejecuta y muestra el Recorrido B (con repetición)
    5. Genera la visualización gráfica
    """
    print("\n" + "=" * 60)
    print("   GESTIÓN DE GRAFO — ESTADOS DE MÉXICO")
    print("   Teoría de Grafos | Ejercicio Académico")
    print("=" * 60 + "\n")

    # Paso 1: Crear el grafo
    G = crear_grafo()

    # Paso 2: Mostrar relaciones (lista de adyacencia)
    mostrar_adyacencia(G)

    # Paso 3: Recorrido A — Camino hamiltoniano
    aristas_hamilton = mostrar_recorrido_a(G)

    # Paso 4: Recorrido B — Con repetición desde CDMX
    aristas_repeticion = mostrar_recorrido_b(G, inicio="Ciudad de México")

    # Paso 5: Visualización
    print("  Generando visualización gráfica...")
    visualizar_grafo(G, aristas_hamilton, aristas_repeticion)

    print("\n  Programa finalizado exitosamente.\n")


# Punto de entrada del programa
if __name__ == "__main__":
    main()
