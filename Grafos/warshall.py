"""
================================================================================
Algoritmo: Warshall - Cerradura Transitiva de un Grafo
================================================================================
Descripción : Determina si existe algún camino (directo o indirecto) entre
              cada par de nodos de un grafo dirigido, produciendo la
              "cerradura transitiva" representada como matriz booleana.
Complejidad : O(V³) en tiempo | O(V²) en espacio
Autor       : Estructura de Datos - Teoría de Grafos
================================================================================
"""

# ==============================================================================
# CLASE PRINCIPAL
# ==============================================================================

class GrafoWarshall:
    """
    Representa un grafo dirigido mediante una MATRIZ DE ADYACENCIA BOOLEANA
    y aplica el algoritmo de Warshall para calcular la cerradura transitiva.

    La cerradura transitiva responde la pregunta:
        "¿Existe ALGÚN camino de i a j, sin importar la longitud?"
    """

    def __init__(self, nodos: list):
        """
        Inicializa el grafo.
        :param nodos: Lista de nombres/etiquetas de los nodos del grafo.
        """
        self.nodos = nodos
        self.n = len(nodos)

        # Mapeo bidireccional: nombre ↔ índice de matriz
        self.indice = {nodo: i for i, nodo in enumerate(nodos)}
        self.nombre = {i: nodo for i, nodo in enumerate(nodos)}

        # Matriz de adyacencia booleana (False = sin arista directa)
        # alcanzable[i][j] = True si existe arista directa de i → j
        self.alcanzable = [[False] * self.n for _ in range(self.n)]

        # La diagonal es True: un nodo siempre se alcanza a sí mismo
        for i in range(self.n):
            self.alcanzable[i][i] = True

    def agregar_arista(self, origen: str, destino: str) -> None:
        """
        Agrega una arista dirigida de origen a destino.
        :param origen:  Nodo de partida.
        :param destino: Nodo de llegada.
        """
        i = self.indice[origen]
        j = self.indice[destino]
        self.alcanzable[i][j] = True

    # --------------------------------------------------------------------------
    # ALGORITMO DE WARSHALL
    # --------------------------------------------------------------------------

    def warshall(self) -> list[list[bool]]:
        """
        Ejecuta el algoritmo de Warshall para calcular la cerradura transitiva.

        Idea central:
          Para cada nodo intermedio k, si se puede llegar de i a k
          Y de k a j, entonces se puede llegar de i a j:
              R[i][j] = R[i][j] OR (R[i][k] AND R[k][j])

        Al finalizar, la matriz resultante indica si existe ALGÚN camino
        (no necesariamente directo) entre cada par de nodos.

        :return: Matriz booleana de la cerradura transitiva.
        """
        # Trabajamos sobre una copia para no alterar la matriz original
        cerradura = [fila[:] for fila in self.alcanzable]

        # Iterar sobre cada nodo k como posible "puente" o intermediario
        for k in range(self.n):
            for i in range(self.n):
                for j in range(self.n):
                    # ¿Se puede ir de i a j pasando por k?
                    if cerradura[i][k] and cerradura[k][j]:
                        cerradura[i][j] = True

        return cerradura

    # --------------------------------------------------------------------------
    # UTILIDADES DE VISUALIZACIÓN
    # --------------------------------------------------------------------------

    def _imprimir_matriz(self, matriz: list[list[bool]], titulo: str) -> None:
        """Imprime una matriz booleana con formato visual claro."""
        ancho = 5
        print(f"\n  {titulo}")
        # Encabezado de columnas
        print("       " + "  ".join(f"{n:^{ancho}}" for n in self.nodos))
        print("     " + "─" * (ancho * self.n + self.n + 2))

        for i in range(self.n):
            fila_vals = []
            for j in range(self.n):
                # Usar '1' y '0' para mayor claridad visual en matrices booleanas
                fila_vals.append(f"{'1' if matriz[i][j] else '0':^{ancho}}")
            print(f"  {self.nodos[i]:<3}| {'  '.join(fila_vals)}")

    def mostrar_resultados(self) -> None:
        """
        Ejecuta Warshall y muestra:
          1. La matriz de adyacencia original.
          2. La cerradura transitiva resultante.
          3. Un resumen textual de las conexiones indirectas descubiertas.
        """
        print("=" * 60)
        print("  ALGORITMO DE WARSHALL — Cerradura Transitiva")
        print("=" * 60)

        # Mostrar la matriz de adyacencia original
        self._imprimir_matriz(self.alcanzable, "Matriz de Adyacencia Original (1 = arista directa):")

        # Calcular la cerradura transitiva
        cerradura = self.warshall()

        # Mostrar la cerradura resultante
        self._imprimir_matriz(cerradura, "Cerradura Transitiva (1 = alcanzable):")

        # Resumen: nuevas conexiones que Warshall descubrió
        print("\n" + "=" * 60)
        print("  Conexiones INDIRECTAS descubiertas por Warshall:")
        print("  (presentes en la cerradura pero no en el grafo original)")
        print("  " + "-" * 50)

        nuevas = False
        for i in range(self.n):
            for j in range(self.n):
                if i != j and cerradura[i][j] and not self.alcanzable[i][j]:
                    print(f"  {self.nodos[i]} →→→ {self.nodos[j]}  (camino indirecto)")
                    nuevas = True

        if not nuevas:
            print("  (No se encontraron nuevas conexiones indirectas)")

        # Tabla de consultas rápidas de accesibilidad
        print("\n" + "=" * 60)
        print("  Tabla de Accesibilidad:")
        print(f"  {'DESDE':<8} {'HACIA':<8} {'¿ALCANZABLE?'}")
        print("  " + "-" * 35)
        for i in range(self.n):
            for j in range(self.n):
                if i != j:
                    resultado = "✓ SÍ" if cerradura[i][j] else "✗ NO"
                    print(f"  {self.nodos[i]:<8} {self.nodos[j]:<8} {resultado}")

        print("=" * 60)

    def puede_alcanzar(self, origen: str, destino: str,
                       cerradura: list[list[bool]]) -> bool:
        """
        Consulta puntual: ¿puede el nodo origen alcanzar al nodo destino?
        :param cerradura: Resultado previo de warshall().
        """
        i = self.indice[origen]
        j = self.indice[destino]
        return cerradura[i][j]


# ==============================================================================
# EJEMPLO DE USO
# ==============================================================================

if __name__ == "__main__":

    # ------------------------------------------------------------------
    # Grafo de prueba dirigido (5 nodos)
    #
    #   A ──► B ──► C
    #   │           │
    #   ▼           ▼
    #   D ──► E     (C → E es la única conexión de C hacia adelante)
    #                ▲
    #                │ (E no tiene salida — nodo sumidero)
    #
    #  Nota: A puede llegar a C (A→B→C), y a E (A→D→E o A→B→C→?...)
    # ------------------------------------------------------------------

    nodos = ["A", "B", "C", "D", "E"]
    grafo = GrafoWarshall(nodos)

    # Definir aristas dirigidas
    aristas = [
        ("A", "B"),
        ("A", "D"),
        ("B", "C"),
        ("C", "E"),
        ("D", "E"),
    ]

    for origen, destino in aristas:
        grafo.agregar_arista(origen, destino)

    # Ejecutar y mostrar todos los resultados
    grafo.mostrar_resultados()

    # ------------------------------------------------------------------
    # Consultas puntuales
    # ------------------------------------------------------------------
    cerradura = grafo.warshall()
    print("\n Consultas puntuales:")
    pares_consulta = [("A", "E"), ("E", "A"), ("B", "D"), ("C", "D")]
    for orig, dest in pares_consulta:
        puede = grafo.puede_alcanzar(orig, dest, cerradura)
        simbolo = "✓" if puede else "✗"
        print(f"  {simbolo}  ¿Puede '{orig}' alcanzar a '{dest}'? → {'SÍ' if puede else 'NO'}")
