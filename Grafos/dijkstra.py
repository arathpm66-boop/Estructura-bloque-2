"""
================================================================================
Algoritmo: Dijkstra - Caminos Mínimos desde un Nodo Origen
================================================================================
Descripción : Encuentra el camino de menor costo desde un nodo fuente hacia
              todos los demás nodos en un grafo ponderado y dirigido/no-dirigido
              con pesos no negativos.
Complejidad : O((V + E) log V) con cola de prioridad | O(V²) versión simple
Autor       : Estructura de Datos - Teoría de Grafos
================================================================================
"""

import heapq  # Módulo estándar para cola de prioridad (min-heap)


# ==============================================================================
# CLASE PRINCIPAL
# ==============================================================================

class GrafoDijkstra:
    """
    Representa un grafo dirigido con pesos usando lista de adyacencia.
    Optimizado para ejecutar el algoritmo de Dijkstra eficientemente.
    """

    def __init__(self, dirigido: bool = False):
        """
        Inicializa el grafo.
        :param dirigido: True si las aristas tienen dirección, False si son bidireccionales.
        """
        self.adyacencia = {}   # Diccionario: nodo -> lista de (vecino, peso)
        self.dirigido = dirigido

    def agregar_nodo(self, nodo: str) -> None:
        """Agrega un nodo al grafo si no existe."""
        if nodo not in self.adyacencia:
            self.adyacencia[nodo] = []

    def agregar_arista(self, origen: str, destino: str, peso: float) -> None:
        """
        Agrega una arista entre origen y destino con el peso dado.
        Si el grafo no es dirigido, agrega la arista en ambas direcciones.
        """
        self.agregar_nodo(origen)
        self.agregar_nodo(destino)
        self.adyacencia[origen].append((destino, peso))

        if not self.dirigido:
            # Para grafos no dirigidos se agrega la arista inversa
            self.adyacencia[destino].append((origen, peso))

    # --------------------------------------------------------------------------
    # ALGORITMO DE DIJKSTRA
    # --------------------------------------------------------------------------

    def dijkstra(self, fuente: str) -> tuple[dict, dict]:
        """
        Ejecuta el algoritmo de Dijkstra desde el nodo fuente.

        Idea central:
          - Se mantiene una cola de prioridad (min-heap) con (distancia, nodo).
          - Siempre se procesa el nodo con menor distancia acumulada.
          - Una vez procesado un nodo, su distancia mínima queda confirmada.

        :param fuente: Nodo de inicio.
        :return: Tupla (distancias, predecesores)
                 distancias  -> distancia mínima desde fuente a cada nodo
                 predecesores -> nodo anterior en el camino óptimo
        """
        if fuente not in self.adyacencia:
            raise ValueError(f"El nodo fuente '{fuente}' no existe en el grafo.")

        # Inicializar todas las distancias como infinito
        distancias = {nodo: float('inf') for nodo in self.adyacencia}
        distancias[fuente] = 0  # La distancia al nodo fuente es 0

        # Guardar el predecesor de cada nodo para reconstruir caminos
        predecesores = {nodo: None for nodo in self.adyacencia}

        # Cola de prioridad: (distancia_acumulada, nodo)
        cola_prioridad = [(0, fuente)]

        # Conjunto de nodos ya procesados (visitados)
        visitados = set()

        while cola_prioridad:
            # Extraer el nodo con menor distancia conocida
            distancia_actual, nodo_actual = heapq.heappop(cola_prioridad)

            # Si ya fue procesado, ignorar (puede haber duplicados en la cola)
            if nodo_actual in visitados:
                continue

            visitados.add(nodo_actual)

            # Relajar las aristas del nodo actual
            for vecino, peso in self.adyacencia[nodo_actual]:
                if vecino in visitados:
                    continue

                nueva_distancia = distancia_actual + peso

                # Si encontramos un camino más corto, actualizamos
                if nueva_distancia < distancias[vecino]:
                    distancias[vecino] = nueva_distancia
                    predecesores[vecino] = nodo_actual
                    heapq.heappush(cola_prioridad, (nueva_distancia, vecino))

        return distancias, predecesores

    def reconstruir_camino(self, predecesores: dict, destino: str) -> list:
        """
        Reconstruye el camino óptimo desde la fuente hasta el destino
        usando el diccionario de predecesores.

        :param predecesores: Diccionario {nodo: predecesor} generado por dijkstra().
        :param destino: Nodo final del camino.
        :return: Lista de nodos que forman el camino óptimo.
        """
        camino = []
        nodo = destino

        # Retroceder desde el destino hasta la fuente
        while nodo is not None:
            camino.append(nodo)
            nodo = predecesores[nodo]

        camino.reverse()  # El camino quedó al revés, lo invertimos

        # Si el camino no comienza con la fuente, no hay ruta válida
        if len(camino) == 1 and predecesores.get(destino) is None and camino[0] != destino:
            return []

        return camino

    def mostrar_resultados(self, fuente: str) -> None:
        """
        Ejecuta Dijkstra y muestra los resultados formateados en consola.
        """
        print("=" * 60)
        print(f"  ALGORITMO DE DIJKSTRA — Fuente: '{fuente}'")
        print("=" * 60)

        distancias, predecesores = self.dijkstra(fuente)

        print(f"\n{'DESTINO':<12} {'DISTANCIA':<15} {'CAMINO ÓPTIMO'}")
        print("-" * 55)

        for nodo in sorted(distancias):
            if nodo == fuente:
                continue

            dist = distancias[nodo]
            camino = self.reconstruir_camino(predecesores, nodo)

            if dist == float('inf'):
                print(f"  {nodo:<10} {'∞':<15} {'Sin conexión'}")
            else:
                ruta = " → ".join(camino)
                print(f"  {nodo:<10} {dist:<15.1f} {ruta}")

        print("=" * 60)


# ==============================================================================
# EJEMPLO DE USO
# ==============================================================================

if __name__ == "__main__":

    # ------------------------------------------------------------------
    # Construir el grafo de prueba (no dirigido, 6 nodos)
    #
    #        2       3
    #   A ——————— B ——————— C
    #   |         |         |
    # 4 |       1 |         | 2
    #   |         |         |
    #   D ——————— E ——————— F
    #        5         1
    # ------------------------------------------------------------------

    grafo = GrafoDijkstra(dirigido=False)

    # Definir aristas: (origen, destino, peso)
    aristas = [
        ("A", "B", 2),
        ("A", "D", 4),
        ("B", "C", 3),
        ("B", "E", 1),
        ("C", "F", 2),
        ("D", "E", 5),
        ("E", "F", 1),
    ]

    for origen, destino, peso in aristas:
        grafo.agregar_arista(origen, destino, peso)

    # Ejecutar Dijkstra desde el nodo "A" y mostrar resultados
    grafo.mostrar_resultados("A")

    # ------------------------------------------------------------------
    # Consulta individual de camino
    # ------------------------------------------------------------------
    print("\n Consulta puntual:")
    distancias, predecesores = grafo.dijkstra("A")
    camino_a_f = grafo.reconstruir_camino(predecesores, "F")
    print(f"  Camino A → F: {' → '.join(camino_a_f)}  (distancia: {distancias['F']})")
