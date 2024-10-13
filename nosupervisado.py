from experta import Fact, Field, Rule, KnowledgeEngine, MATCH
from sklearn.cluster import KMeans
import numpy as np

# Definir la clase Ruta con unidades de kilómetros, minutos y pesos COP
class Ruta(Fact):
    """Definir una ruta entre dos puntos"""
    origen = Field(str, mandatory=True)
    destino = Field(str, mandatory=True)
    distancia = Field(int, mandatory=True)  # en kilómetros
    tiempo = Field(int, mandatory=True)  # en minutos
    costo = Field(float, mandatory=True)  # en pesos COP

class Criterio(Fact):
    """Criterio de selección de la mejor ruta"""
    tipo = Field(str, mandatory=True)

class SistemaTransporte(KnowledgeEngine):
    @Rule(Criterio(tipo='menor_tiempo'),
          Ruta(origen=MATCH.origen, destino=MATCH.destino, tiempo=MATCH.tiempo, costo=MATCH.costo,
               distancia=MATCH.distancia))
    def seleccionar_por_tiempo(self, origen, destino, tiempo, costo, distancia):
        print(f"Ruta rápida entre {origen} y {destino}: {tiempo} minutos, {distancia} km, costo {costo} COP.")

    @Rule(Criterio(tipo='menor_costo'),
          Ruta(origen=MATCH.origen, destino=MATCH.destino, tiempo=MATCH.tiempo, costo=MATCH.costo,
               distancia=MATCH.distancia))
    def seleccionar_por_costo(self, origen, destino, tiempo, costo, distancia):
        print(f"Ruta económica entre {origen} y {destino}: {costo} COP, {tiempo} minutos, {distancia} km.")

    @Rule(Criterio(tipo='menor_distancia'),
          Ruta(origen=MATCH.origen, destino=MATCH.destino, tiempo=MATCH.tiempo, costo=MATCH.costo,
               distancia=MATCH.distancia))
    def seleccionar_por_distancia(self, origen, destino, tiempo, costo, distancia):
        print(f"Ruta corta entre {origen} y {destino}: {distancia} km, {tiempo} minutos, costo {costo} COP.")

# Inicializar el motor de reglas
sistema = SistemaTransporte()

# Rutas posibles (con las unidades ajustadas)
sistema.reset()

# Crear una lista de datos (distancia, tiempo, costo)
rutas_data = [
    [10, 15, 2500],
    [12, 20, 2000],
    [8, 18, 3000],
    [15, 25, 3500],
    [17, 30, 2800]
]

# Crear un modelo KMeans para 2 clusters
kmeans = KMeans(n_clusters=2)
kmeans.fit(rutas_data)

# Declarar las rutas con los resultados del clustering
rutas = [
    Ruta(origen='A', destino='B', distancia=10, tiempo=15, costo=2500.0),
    Ruta(origen='A', destino='B', distancia=12, tiempo=20, costo=2000.0),
    Ruta(origen='A', destino='B', distancia=8, tiempo=18, costo=3000.0),
    Ruta(origen='A', destino='C', distancia=15, tiempo=25, costo=3500.0),
    Ruta(origen='A', destino='C', distancia=17, tiempo=30, costo=2800.0)
]

clusters = kmeans.predict(rutas_data)

# Mostrar las rutas y sus clusters
for i, ruta in enumerate(rutas):
    print(f"Ruta de {ruta['origen']} a {ruta['destino']} -> Cluster {clusters[i]}, "
          f"Distancia: {ruta['distancia']} km, Tiempo: {ruta['tiempo']} minutos, Costo: {ruta['costo']} COP.")

# Declarar el criterio de selección por menor tiempo
print("\nSeleccionando rutas del cluster con menor tiempo:")
sistema.declare(Criterio(tipo='menor_tiempo'))

# Declarar las rutas seleccionadas por cluster
for i, ruta in enumerate(rutas):
    if clusters[i] == np.argmin(kmeans.cluster_centers_[:, 1]):  # Cluster con menor tiempo promedio
        sistema.declare(ruta)

sistema.run()
