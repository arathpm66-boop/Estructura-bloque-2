# ============================================================
# Implementación de una Cola con Listas Enlazadas
# Sistema de recepción de pedidos de empresa
# ============================================================


class Order:
    """
    Clase que representa un pedido de cliente.
    Equivalente a la clase Order en Java.
    """
    def __init__(self, qtty: int, customer: str):
        self.customer = customer
        self.qtty = qtty

    def print_order(self):
        print(f"     Customer: {self.get_customer()}")
        print(f"     Quantity: {self.get_qtty()}")
        print("     ------------")

    def get_qtty(self) -> int:
        return self.qtty

    def get_customer(self) -> str:
        return self.customer


# ============================================================
# Nodo de la lista enlazada
# ============================================================

class Node:
    """
    Nodo que almacena un pedido y apunta al siguiente nodo.
    """
    def __init__(self, order: Order):
        self.order = order
        self.next = None  # Puntero al siguiente nodo


# ============================================================
# Cola implementada con lista enlazada (FIFO)
# ============================================================

class OrderQueue:
    """
    Cola de pedidos implementada con lista enlazada.
    FIFO: El primer pedido en entrar es el primero en procesarse.
    """
    def __init__(self):
        self.front = None  # Nodo al frente (para dequeue)
        self.rear = None   # Nodo al final (para enqueue)
        self.size = 0

    def is_empty(self) -> bool:
        """Verifica si la cola está vacía."""
        return self.front is None

    def enqueue(self, order: Order):
        """Agrega un pedido al final de la cola."""
        new_node = Node(order)
        if self.rear is None:
            self.front = new_node
            self.rear = new_node
        else:
            self.rear.next = new_node
            self.rear = new_node
        self.size += 1
        print(f"  ✔ Pedido de '{order.get_customer()}' agregado a la cola.")

    def dequeue(self) -> Order:
        """Elimina y retorna el pedido al frente de la cola."""
        if self.is_empty():
            print("  ✖ La cola está vacía. No hay pedidos que procesar.")
            return None
        order = self.front.order
        self.front = self.front.next
        if self.front is None:
            self.rear = None
        self.size -= 1
        return order

    def peek(self) -> Order:
        """Retorna el pedido al frente sin eliminarlo."""
        if self.is_empty():
            print("  ✖ La cola está vacía.")
            return None
        return self.front.order

    def display(self):
        """Muestra todos los pedidos en la cola."""
        if self.is_empty():
            print("  La cola está vacía.")
            return
        print(f"  Cola de pedidos ({self.size} pedido(s)):")
        print("  ============================================")
        current = self.front
        position = 1
        while current is not None:
            print(f"  Pedido #{position}:")
            current.order.print_order()
            current = current.next
            position += 1


# ============================================================
# Sección interactiva: insertar y eliminar N pedidos
# ============================================================

def ingresar_n_pedidos(cola: OrderQueue):
    """Pregunta cuántos pedidos agregar, muestra resumen y pide confirmación."""
    while True:
        try:
            n = int(input("\n  ¿Cuántos pedidos desea agregar? (0 = regresar al menú): "))
            if n == 0:
                print("  ↩ Regresando al menú sin cambios...")
                return
            if n < 0:
                print("  ⚠ Ingrese un número mayor a 0.")
                continue
            break
        except ValueError:
            print("  ⚠ Ingrese un número entero válido.")

    # Recopilar pedidos temporalmente sin tocar la cola aún
    pedidos_temp = []
    print()
    for i in range(1, n + 1):
        print(f"  -- Pedido {i} de {n} --")
        customer = input("     Nombre del cliente (0 = regresar al menú): ").strip()
        if customer == "0":
            print("  ↩ Regresando al menú sin cambios...")
            return
        while True:
            try:
                qtty = int(input("     Cantidad solicitada: "))
                if qtty <= 0:
                    print("     ⚠ La cantidad debe ser mayor a 0.")
                    continue
                break
            except ValueError:
                print("     ⚠ Ingrese un número entero válido.")
        pedidos_temp.append(Order(qtty, customer))

    # Mostrar resumen y pedir confirmación
    print(f"\n  📋 Resumen de pedidos a insertar:")
    print("  " + "-" * 38)
    for idx, p in enumerate(pedidos_temp, 1):
        print(f"  Pedido #{idx}:")
        p.print_order()

    while True:
        confirm = input("  ¿Confirma la inserción? (s = sí / n = regresar al menú): ").strip().lower()
        if confirm == "s":
            for p in pedidos_temp:
                cola.enqueue(p)
            print(f"\n  ✅ {n} pedido(s) agregado(s) correctamente.")
            break
        elif confirm == "n":
            print("  ↩ Inserción cancelada. Regresando al menú sin cambios...")
            break
        else:
            print("  ⚠ Ingrese 's' para confirmar o 'n' para cancelar.")


def eliminar_n_pedidos(cola: OrderQueue):
    """Pregunta cuántos pedidos eliminar, muestra cuáles serán y pide confirmación."""
    if cola.is_empty():
        print("\n  ✖ La cola está vacía. No hay pedidos que eliminar.")
        return

    print(f"\n  Hay {cola.size} pedido(s) en la cola.")
    while True:
        try:
            n = int(input("  ¿Cuántos pedidos desea eliminar? (0 = regresar al menú): "))
            if n == 0:
                print("  ↩ Regresando al menú sin cambios...")
                return
            if n < 0:
                print("  ⚠ Ingrese un número mayor a 0.")
                continue
            if n > cola.size:
                print(f"  ⚠ Solo hay {cola.size} pedido(s). Ingrese un número menor o igual.")
                continue
            break
        except ValueError:
            print("  ⚠ Ingrese un número entero válido.")

    # Mostrar cuáles pedidos serán eliminados antes de confirmar
    print(f"\n  📋 Los siguientes {n} pedido(s) serán eliminados:")
    print("  " + "-" * 38)
    current = cola.front
    for i in range(n):
        print(f"  Pedido #{i + 1}:")
        current.order.print_order()
        current = current.next

    while True:
        confirm = input("  ¿Confirma la eliminación? (s = sí / n = regresar al menú): ").strip().lower()
        if confirm == "s":
            print(f"\n  ⚙️  Eliminando {n} pedido(s)...")
            print("  " + "-" * 38)
            for i in range(n):
                pedido = cola.dequeue()
                print(f"\n  ✅ Pedido #{i + 1} procesado:")
                pedido.print_order()
            print(f"\n  {n} pedido(s) eliminado(s). Quedan {cola.size} en la cola.")
            break
        elif confirm == "n":
            print("  ↩ Eliminación cancelada. Regresando al menú sin cambios...")
            break
        else:
            print("  ⚠ Ingrese 's' para confirmar o 'n' para cancelar.")


def menu_interactivo(cola: OrderQueue):
    """Menú principal de la sección interactiva."""
    print("\n" + "=" * 52)
    print("   SECCIÓN INTERACTIVA")
    print("=" * 52)

    while True:
        print("\n  ¿Qué desea hacer?")
        print("  [1] Insertar N pedidos")
        print("  [2] Eliminar N pedidos")
        print("  [3] Ver cola actual")
        print("  [4] Salir")
        opcion = input("\n  Opción: ").strip()

        if opcion == "1":
            ingresar_n_pedidos(cola)
        elif opcion == "2":
            eliminar_n_pedidos(cola)
        elif opcion == "3":
            print()
            cola.display()
        elif opcion == "4":
            print("\n  👋 Saliendo del sistema.")
            break
        else:
            print("  ⚠ Opción no válida. Elija entre 1 y 4.")


# ============================================================
# Simulación del sistema de pedidos
# ============================================================

def main():
    print("=" * 52)
    print("   SISTEMA DE PEDIDOS - EMPRESA XYZ")
    print("=" * 52)

    cola = OrderQueue()

    # --- Llegada de pedidos ---
    print("\n📥 RECEPCIÓN DE PEDIDOS:")
    print("-" * 40)
    cola.enqueue(Order(100, "Empresa Alpha"))
    cola.enqueue(Order(250, "Empresa Beta"))
    cola.enqueue(Order(75,  "Empresa Gamma"))
    cola.enqueue(Order(500, "Empresa Delta"))

    # --- Estado actual de la cola ---
    print("\n📋 ESTADO ACTUAL DE LA COLA:")
    print("-" * 40)
    cola.display()

    # --- Próximo en ser procesado ---
    proximo = cola.peek()
    if proximo:
        print(f"\n🔍 Próximo pedido a procesar: '{proximo.get_customer()}'")

    # --- Procesamiento de pedidos ---
    print("\n⚙️  PROCESANDO PEDIDOS (FIFO):")
    print("-" * 40)

    while not cola.is_empty():
        pedido = cola.dequeue()
        print(f"\n  ✅ Procesando pedido de: '{pedido.get_customer()}'")
        pedido.print_order()

    # --- Cola vacía ---
    print("\n📭 COLA FINAL:")
    print("-" * 40)
    cola.display()

    # --- Intento de dequeue en cola vacía ---
    print("\n⚠️  Intentando procesar pedido en cola vacía:")
    cola.dequeue()

    print("\n" + "=" * 52)
    print("   FIN DE LA SIMULACIÓN AUTOMÁTICA")
    print("=" * 52)

    # --- Sección interactiva ---
    menu_interactivo(cola)


if __name__ == "__main__":
    main()
