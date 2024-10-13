from experta import *


class Ruta(Fact):
    """Definir una ruta entre dos puntos"""
    origen = Field(str, mandatory=True)
    destino = Field(str, mandatory=True)
    distancia = Field(int, mandatory=True)  # en kilómetros
    tiempo = Field(int, mandatory=True)  # en minutos
    costo = Field(float, mandatory=True)  # en unidades monetarias


class Criterio(Fact):
    """Criterio de selección de la mejor ruta"""
    tipo = Field(str, mandatory=True)


class SistemaTransporte(KnowledgeEngine):
    def __init__(self):
        super().__init__()
        self.mejor_ruta = None

    # Selección por menor tiempo
    @Rule(Criterio(tipo='menor_tiempo'),
          Ruta(origen=MATCH.origen, destino=MATCH.destino, tiempo=MATCH.tiempo, costo=MATCH.costo,
               distancia=MATCH.distancia))
    def seleccionar_por_tiempo(self, origen, destino, tiempo, costo, distancia):
        if self.mejor_ruta is None or tiempo < self.mejor_ruta['tiempo']:
            self.mejor_ruta = {'origen': origen, 'destino': destino, 'tiempo': tiempo, 'costo': costo,
                               'distancia': distancia}

    # Selección por menor costo
    @Rule(Criterio(tipo='menor_costo'),
          Ruta(origen=MATCH.origen, destino=MATCH.destino, tiempo=MATCH.tiempo, costo=MATCH.costo,
               distancia=MATCH.distancia))
    def seleccionar_por_costo(self, origen, destino, tiempo, costo, distancia):
        if self.mejor_ruta is None or costo < self.mejor_ruta['costo']:
            self.mejor_ruta = {'origen': origen, 'destino': destino, 'tiempo': tiempo, 'costo': costo,
                               'distancia': distancia}

    # Selección por menor distancia
    @Rule(Criterio(tipo='menor_distancia'),
          Ruta(origen=MATCH.origen, destino=MATCH.destino, tiempo=MATCH.tiempo, costo=MATCH.costo,
               distancia=MATCH.distancia))
    def seleccionar_por_distancia(self, origen, destino, tiempo, costo, distancia):
        if self.mejor_ruta is None or distancia < self.mejor_ruta['distancia']:
            self.mejor_ruta = {'origen': origen, 'destino': destino, 'tiempo': tiempo, 'costo': costo,
                               'distancia': distancia}

    # Mostrar la mejor ruta al finalizar la selección
    def mostrar_mejor_ruta(self):
        if self.mejor_ruta:
            print(f"Mejor ruta entre {self.mejor_ruta['origen']} y {self.mejor_ruta['destino']}:")
            print(f"  Tiempo: {self.mejor_ruta['tiempo']} minutos")
            print(f"  Distancia: {self.mejor_ruta['distancia']} km")
            print(f"  Costo: {self.mejor_ruta['costo']} unidades")


# Inicializar el motor de reglas
sistema = SistemaTransporte()

# Declarar las rutas posibles
sistema.reset()

# Rutas posibles
sistema.declare(Ruta(origen='A', destino='B', distancia=10, tiempo=15, costo=2.5))
sistema.declare(Ruta(origen='A', destino='B', distancia=12, tiempo=20, costo=2.0))
sistema.declare(Ruta(origen='A', destino='B', distancia=8, tiempo=18, costo=3.0))
sistema.declare(Ruta(origen='A', destino='C', distancia=15, tiempo=25, costo=3.5))
sistema.declare(Ruta(origen='A', destino='C', distancia=17, tiempo=30, costo=2.8))

# Declarar el criterio de selección y ejecutar el sistema
print("\nSeleccionando por menor tiempo:")
sistema.declare(Criterio(tipo='menor_tiempo'))
sistema.run()
sistema.mostrar_mejor_ruta()

# Resetear para el siguiente criterio
sistema.mejor_ruta = None

print("\nSeleccionando por menor costo:")
sistema.declare(Criterio(tipo='menor_costo'))
sistema.run()
sistema.mostrar_mejor_ruta()

# Resetear para el siguiente criterio
sistema.mejor_ruta = None

print("\nSeleccionando por menor distancia:")
sistema.declare(Criterio(tipo='menor_distancia'))
sistema.run()
sistema.mostrar_mejor_ruta()
