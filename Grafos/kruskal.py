"""
================================================================================
Algoritmo: Kruskal - Árbol de Expansión Mínima (MST)
================================================================================
Descripción : Construye el Árbol de Expansión Mínima (Minimum Spanning Tree)
              de un grafo no dirigido y ponderado, seleccionando las aristas
              de menor peso que conectan todos los nodos sin formar ciclos.
              Usa la estructura Union-Find (Conjuntos Disjuntos) internamente.
Complejidad : O(E log E) por la ordenación de aristas
Autor       : Estructura de Datos - Teoría de Grafos
================================================================================
"""

# ==============================================================================
# ESTRUCTURA AUXILIAR: UNION-FIND (Conjuntos Disjuntos)
# ==============================================================================

class UnionFind:
    """
    Estructura de datos de Conjuntos Disjuntos (Disjoint Set Union).

    Permite saber eficientemente si dos nodos están en el mismo componente
    conectado, y unir dos componentes en O(α(n)) ≈ O(1) amortizado.

    Kruskal la usa para detectar si agregar una arista crearía un ciclo:
    si los dos extremos ya están en el mismo componente → ciclo.
    """

    def __init__(self, nodos: list):
        """
        Inicializa cada nodo como su propio representante (su propio componente).
        :param nodos: Lista de nodos del grafo.
        """
        # Cada nodo apunta a sí mismo como padre (bosque de árboles)
        self.padre = {nodo: nodo for nodo in nodos}

        # Rango: controla la altura del árbol para mantener la estructura plana
        self.rango = {nodo: 0 for nodo in nodos}

    def encontrar(self, nodo: str) -> str:
        """
        Encuentra el representante (raíz) del componente al que pertenece el nodo.
        Aplica "compresión de camino": aplana el árbol para futuras búsquedas.

        :param nodo: Nodo a consultar.
        :return: Representante del componente.
        """
        if self.padre[nodo] != nodo:
            # Compresión de camino: el padre pasa a ser directamente la raíz
            self.padre[nodo] = self.encontrar(self.padre[nodo])
        return self.padre[nodo]

    def unir(self, nodo_a: str, nodo_b: str) -> bool:
        """
        Une los componentes de nodo_a y nodo_b.
        Usa "unión por rango" para mantener los árboles balanceados.

        :return: True si se unieron componentes distintos (no había ciclo).
                 False si ya estaban en el mismo componente (habría ciclo).
        """
        raiz_a = self.encontrar(nodo_a)
        raiz_b = self.encontrar(nodo_b)

        if raiz_a == raiz_b:
            return False  # Ya están conectados → agregar esta arista crearía un ciclo

        # Unión por rango: el árbol más "alto" absorbe al más "bajo"
        if self.rango[raiz_a] < self.rango[raiz_b]:
            raiz_a, raiz_b = raiz_b, raiz_a  # Intercambiar para que raiz_a sea el mayor

        self.padre[raiz_b] = raiz_a  # raiz_b queda bajo raiz_a

        # Si tenían el mismo rango, el árbol resultante crece en altura
        if self.rango[raiz_a] == self.rango[raiz_b]:
            self.rango[raiz_a] += 1

        return True


# ==============================================================================
# CLASE PRINCIPAL
# ==============================================================================

class GrafoKruskal:
    """
    Representa un grafo no dirigido y ponderado, y aplica el algoritmo
    de Kruskal para encontrar el Árbol de Expansión Mínima (MST).
    """

    def __init__(self):
        """Inicializa el grafo con conjuntos vacíos de nodos y aristas."""
        self.nodos = set()
        self.aristas = []  # Lista de (peso, origen, destino)

    def agregar_arista(self, origen: str, destino: str, peso: float) -> None:
        """
        Agrega una arista no dirigida al grafo.
        :param origen:  Primer extremo de la arista.
        :param destino: Segundo extremo de la arista.
        :param peso:    Costo de la arista.
        """
        self.nodos.add(origen)
        self.nodos.add(destino)
        self.aristas.append((peso, origen, destino))

    # --------------------------------------------------------------------------
    # ALGORITMO DE KRUSKAL
    # --------------------------------------------------------------------------

    def kruskal(self) -> tuple[list, float]:
        """
        Ejecuta el algoritmo de Kruskal para construir el MST.

        Pasos:
          1. Ordenar todas las aristas de menor a mayor peso.
          2. Iterar sobre las aristas; agregar al MST aquellas que
             NO formen ciclos (verificado con Union-Find).
          3. Detenerse cuando el MST tenga V-1 aristas.

        :return: Tupla (mst, costo_total)
                 mst        -> lista de aristas del MST: [(peso, origen, destino)]
                 costo_total -> suma de los pesos del MST
        """
        # Paso 1: Ordenar aristas por peso (ascendente)
        aristas_ordenadas = sorted(self.aristas, key=lambda x: x[0])

        # Inicializar Union-Find con todos los nodos
        uf = UnionFind(list(self.nodos))

        mst = []           # Aristas seleccionadas para el MST
        costo_total = 0    # Costo acumulado del MST

        # Paso 2: Procesar cada arista en orden de peso
        for peso, origen, destino in aristas_ordenadas:

            # Intentar unir los componentes de origen y destino
            if uf.unir(origen, destino):
                # No había ciclo → agregar al MST
                mst.append((peso, origen, destino))
                costo_total += peso

                # Paso 3: El MST está completo cuando tiene V-1 aristas
                if len(mst) == len(self.nodos) - 1:
                    break

        # Verificar si el grafo era conexo (el MST debe tener V-1 aristas)
        if len(mst) < len(self.nodos) - 1:
            print("  ⚠ ADVERTENCIA: El grafo no es conexo. MST incompleto.")

        return mst, costo_total

    def mostrar_resultados(self) -> None:
        """
        Ejecuta Kruskal y muestra las aristas del MST con su costo total.
        """
        print("=" * 58)
        print("  ALGORITMO DE KRUSKAL — Árbol de Expansión Mínima (MST)")
        print("=" * 58)

        print(f"\n  Nodos del grafo   : {sorted(self.nodos)}")
        print(f"  Total de aristas  : {len(self.aristas)}")

        # Mostrar todas las aristas ordenadas
        print("\n  Aristas disponibles (ordenadas por peso):")
        print(f"  {'PESO':<8} {'ORIGEN':<10} {'DESTINO'}")
        print("  " + "-" * 30)
        for peso, origen, destino in sorted(self.aristas):
            print(f"  {peso:<8.1f} {origen:<10} {destino}")

        # Ejecutar Kruskal
        mst, costo_total = self.kruskal()

        # Mostrar las aristas seleccionadas para el MST
        print("\n" + "=" * 58)
        print("  Aristas seleccionadas para el MST:")
        print(f"  {'PASO':<6} {'PESO':<8} {'ARISTA':<20} {'ACCIÓN'}")
        print("  " + "-" * 50)

        acumulado = 0
        for paso, (peso, origen, destino) in enumerate(mst, 1):
            acumulado += peso
            arista = f"{origen} ── {destino}"
            print(f"  {paso:<6} {peso:<8.1f} {arista:<20} ✓ Añadida (acum: {acumulado:.1f})")

        print("\n" + "=" * 58)
        print(f"  Aristas en el MST : {len(mst)}")
        print(f"  COSTO TOTAL MST   : {costo_total:.1f}")
        print("=" * 58)

        # Representación visual del MST como lista de adyacencia
        print("\n  Árbol de Expansión Mínima (lista de adyacencia):")
        adj_mst = {nodo: [] for nodo in self.nodos}
        for peso, origen, destino in mst:
            adj_mst[origen].append(f"{destino}({peso:.0f})")
            adj_mst[destino].append(f"{origen}({peso:.0f})")

        for nodo in sorted(adj_mst):
            vecinos = ", ".join(sorted(adj_mst[nodo]))
            print(f"    {nodo}: [{vecinos}]")

        print("=" * 58)


# ==============================================================================
# EJEMPLO DE USO
# ==============================================================================

if __name__ == "__main__":

    # ------------------------------------------------------------------
    # Grafo de prueba no dirigido (6 nodos, 9 aristas)
    #
    #       4         2
    #   A ───── B ───── C
    #   │ \     │     / │
    #   │  \8   │1  /5  │3
    #   6   \   │ /     │
    #   │    \  │/      │
    #   D ───── E ───── F
    #       7         9
    #
    #  MST esperado: B-E(1), B-C(2), C-F(3), A-B(4), A-D(6) = 16
    # ------------------------------------------------------------------

    grafo = GrafoKruskal()

    # Aristas: (origen, destino, peso)
    aristas = [
        ("A", "B", 4),
        ("A", "D", 6),
        ("A", "E", 8),
        ("B", "C", 2),
        ("B", "E", 1),
        ("C", "E", 5),
        ("C", "F", 3),
        ("D", "E", 7),
        ("E", "F", 9),
    ]

    for origen, destino, peso in aristas:
        grafo.agregar_arista(origen, destino, peso)

    # Ejecutar y mostrar resultados
    grafo.mostrar_resultados()
