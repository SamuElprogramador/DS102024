class Modelo:
    """
    Esta es una clase de ejemplo que representa un modelo muy simple.
    """

    def __init__(self, nombre):
        self.nombre = nombre

    def describir(self):
        """
        Esta función devuelve una descripción del modelo.
        """
        return f"Este es un modelo llamado {self.nombre}."

def multiplicar(a, b):
    """
    Esta función toma dos números y devuelve su producto.
    """
    return a * b