"""
================================================================================
Algoritmo: Floyd-Warshall - Caminos Mínimos entre Todos los Pares de Nodos
================================================================================
Descripción : Calcula las distancias mínimas entre TODOS los pares de nodos
              en un grafo ponderado (dirigido o no dirigido), incluyendo
              detección de ciclos negativos.
Complejidad : O(V³) en tiempo | O(V²) en espacio
Autor       : Estructura de Datos - Teoría de Grafos
================================================================================
"""

# ==============================================================================
# CONSTANTE
# ==============================================================================

INF = float('inf')  # Representación de "sin conexión directa"


# ==============================================================================
# CLASE PRINCIPAL
# ==============================================================================

class GrafoFloydWarshall:
    """
    Representa un grafo mediante una MATRIZ DE ADYACENCIA y aplica
    el algoritmo de Floyd-Warshall para encontrar los caminos mínimos
    entre todos los pares de nodos.
    """

    def __init__(self, nodos: list):
        """
        Inicializa el grafo con la lista de nodos dada.

        :param nodos: Lista de nombres/etiquetas de los nodos.
        """
        self.nodos = nodos
        self.n = len(nodos)

        # Mapeo de nombre de nodo a índice de matriz y viceversa
        self.indice = {nodo: i for i, nodo in enumerate(nodos)}
        self.nombre = {i: nodo for i, nodo in enumerate(nodos)}

        # Inicializar la matriz de distancias:
        #   - 0 en la diagonal (distancia de un nodo a sí mismo)
        #   - INF donde no hay arista directa
        self.dist = [[INF] * self.n for _ in range(self.n)]
        for i in range(self.n):
            self.dist[i][i] = 0

        # Matriz de predecesores para reconstruir caminos
        # next_hop[i][j] = siguiente nodo en el camino óptimo de i a j
        self.next_hop = [[None] * self.n for _ in range(self.n)]

    def agregar_arista(self, origen: str, destino: str, peso: float,
                       dirigido: bool = False) -> None:
        """
        Registra una arista en la matriz de adyacencia.

        :param origen:   Nodo de partida.
        :param destino:  Nodo de llegada.
        :param peso:     Costo/peso de la arista.
        :param dirigido: Si es False, se agrega también la arista inversa.
        """
        i, j = self.indice[origen], self.indice[destino]

        # Solo actualizamos si el nuevo peso es mejor (por si hay aristas paralelas)
        if peso < self.dist[i][j]:
            self.dist[i][j] = peso
            self.next_hop[i][j] = j  # El siguiente salto directo es el propio destino

        if not dirigido and peso < self.dist[j][i]:
            self.dist[j][i] = peso
            self.next_hop[j][i] = i

    # --------------------------------------------------------------------------
    # ALGORITMO DE FLOYD-WARSHALL
    # --------------------------------------------------------------------------

    def floyd_warshall(self) -> bool:
        """
        Ejecuta el algoritmo de Floyd-Warshall.

        Idea central:
          Para cada nodo intermedio k, verificamos si pasar por k
          mejora el camino entre cada par (i, j):
              dist[i][j] = min(dist[i][j], dist[i][k] + dist[k][j])

        :return: True si el grafo no tiene ciclos negativos, False si los tiene.
        """
        n = self.n

        # Iterar sobre cada nodo candidato a ser "nodo intermedio"
        for k in range(n):
            for i in range(n):
                for j in range(n):
                    # Verificar si la ruta i -> k -> j es más corta que i -> j
                    if self.dist[i][k] != INF and self.dist[k][j] != INF:
                        nueva_dist = self.dist[i][k] + self.dist[k][j]
                        if nueva_dist < self.dist[i][j]:
                            self.dist[i][j] = nueva_dist
                            self.next_hop[i][j] = self.next_hop[i][k]

        # Detectar ciclos negativos: si dist[i][i] < 0, hay un ciclo negativo
        ciclo_negativo = any(self.dist[i][i] < 0 for i in range(n))
        return not ciclo_negativo

    def reconstruir_camino(self, origen: str, destino: str) -> list:
        """
        Reconstruye el camino óptimo entre dos nodos usando next_hop.

        :param origen:  Nodo de inicio.
        :param destino: Nodo de llegada.
        :return: Lista de nodos del camino, o [] si no hay ruta.
        """
        i, j = self.indice[origen], self.indice[destino]

        if self.next_hop[i][j] is None:
            return []  # Sin camino

        camino = [origen]
        while i != j:
            i = self.next_hop[i][j]
            camino.append(self.nombre[i])

        return camino

    def mostrar_matriz(self, titulo: str, matriz: list) -> None:
        """Imprime una matriz cuadrada con formato tabular."""
        ancho_col = 8
        print(f"\n  {titulo}")
        print("  " + " " * 6 + "  ".join(f"{n:^{ancho_col}}" for n in self.nodos))
        print("  " + "-" * (ancho_col * self.n + 10))

        for i, fila in enumerate(matriz):
            valores = []
            for v in fila:
                if v == INF:
                    valores.append(f"{'∞':^{ancho_col}}")
                else:
                    valores.append(f"{v:^{ancho_col}.0f}")
            print(f"  {self.nodos[i]:<4} | {'  '.join(valores)}")

    def mostrar_resultados(self) -> None:
        """
        Ejecuta Floyd-Warshall y muestra: matriz de distancias y
        todos los caminos mínimos entre pares.
        """
        print("=" * 65)
        print("  ALGORITMO DE FLOYD-WARSHALL")
        print("=" * 65)

        sin_ciclos = self.floyd_warshall()

        if not sin_ciclos:
            print("\n  ⚠ ADVERTENCIA: Se detectó un ciclo negativo. Los resultados")
            print("    pueden no ser válidos.")
            return

        # Mostrar la matriz de distancias resultante
        self.mostrar_matriz("Matriz de Distancias Mínimas:", self.dist)

        # Mostrar todos los caminos entre pares
        print("\n" + "=" * 65)
        print(f"  {'ORIGEN':<8} {'DESTINO':<10} {'DIST':<8} {'CAMINO ÓPTIMO'}")
        print("  " + "-" * 55)

        for origen in self.nodos:
            for destino in self.nodos:
                if origen == destino:
                    continue
                i, j = self.indice[origen], self.indice[destino]
                dist = self.dist[i][j]
                camino = self.reconstruir_camino(origen, destino)

                if dist == INF or not camino:
                    print(f"  {origen:<8} {destino:<10} {'∞':<8} Sin conexión")
                else:
                    ruta = " → ".join(camino)
                    print(f"  {origen:<8} {destino:<10} {dist:<8.0f} {ruta}")

        print("=" * 65)


# ==============================================================================
# EJEMPLO DE USO
# ==============================================================================

if __name__ == "__main__":

    # ------------------------------------------------------------------
    # Grafo de prueba (dirigido, 5 nodos)
    #
    #    ┌──────────────────────────────────┐
    #    │   A ──3──► B ──2──► C           │
    #    │   │        │         ▲           │
    #    │   8        1         │           │
    #    │   │        │         5           │
    #    │   ▼        ▼         │           │
    #    │   D ──4──► E ────────┘           │
    #    └──────────────────────────────────┘
    # ------------------------------------------------------------------

    nodos = ["A", "B", "C", "D", "E"]
    grafo = GrafoFloydWarshall(nodos)

    # Aristas dirigidas: (origen, destino, peso)
    aristas = [
        ("A", "B", 3),
        ("A", "D", 8),
        ("B", "C", 2),
        ("B", "E", 1),
        ("D", "E", 4),
        ("E", "C", 5),
    ]

    for origen, destino, peso in aristas:
        grafo.agregar_arista(origen, destino, peso, dirigido=True)

    # Ejecutar y mostrar resultados
    grafo.mostrar_resultados()

    # ------------------------------------------------------------------
    # Consulta puntual entre dos nodos específicos
    # ------------------------------------------------------------------
    grafo.floyd_warshall()  # Aseguramos que el algoritmo ya corrió
    print("\n Consulta puntual:")
    i_a, i_c = grafo.indice["A"], grafo.indice["C"]
    camino = grafo.reconstruir_camino("A", "C")
    print(f"  Camino A → C: {' → '.join(camino)}  (distancia: {grafo.dist[i_a][i_c]:.0f})")
