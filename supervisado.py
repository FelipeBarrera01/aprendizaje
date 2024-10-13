import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
from imblearn.over_sampling import SMOTE

# Crear un dataset de rutas con variables de tiempo, costo y distancia
np.random.seed(42)
n = 1000

# Variables simuladas
origenes = np.random.choice(['A', 'B', 'C', 'D'], size=n)
destinos = np.random.choice(['A', 'B', 'C', 'D'], size=n)
tiempos = np.random.randint(5, 120, size=n)  # tiempos entre 5 y 120 minutos
costos = np.random.uniform(1, 100, size=n)   # costos entre 1 y 100 unidades
distancias = np.random.randint(1, 500, size=n)  # distancias entre 1 y 500 km

# Crear una función para expandir los valores mínimos de cada grupo de 10 elementos
def expand_minimums(arr, group_size):
    min_values = np.minimum.reduceat(arr, np.arange(0, len(arr), group_size))
    expanded_min = np.repeat(min_values, group_size)
    return expanded_min[:len(arr)]  # Cortamos en caso de que el último bloque no sea múltiplo de 10

# Etiquetas simuladas (1 = mejor ruta, 0 = no es la mejor ruta)
y_tiempo = (tiempos == expand_minimums(tiempos, 10)).astype(int)
y_costo = (costos == expand_minimums(costos, 10)).astype(int)
y_distancia = (distancias == expand_minimums(distancias, 10)).astype(int)

# Crear el dataset de características
X = np.column_stack([origenes, destinos, tiempos, costos, distancias])

# Dividir los datos en entrenamiento y prueba
X_train, X_test, y_train_tiempo, y_test_tiempo = train_test_split(X, y_tiempo, test_size=0.2, random_state=42)
_, _, y_train_costo, y_test_costo = train_test_split(X, y_costo, test_size=0.2, random_state=42)
_, _, y_train_distancia, y_test_distancia = train_test_split(X, y_distancia, test_size=0.2, random_state=42)

# Convertir a formato numérico adecuado (por simplicidad, ignoramos origen/destino)
X_train_numeric = X_train[:, 2:].astype(float)  # Usamos tiempo, costo, distancia
X_test_numeric = X_test[:, 2:].astype(float)

# Aplicar SMOTE para balancear las clases
smote = SMOTE(random_state=42)
X_train_smote, y_train_tiempo_smote = smote.fit_resample(X_train_numeric, y_train_tiempo)
X_train_smote_costo, y_train_costo_smote = smote.fit_resample(X_train_numeric, y_train_costo)
X_train_smote_distancia, y_train_distancia_smote = smote.fit_resample(X_train_numeric, y_train_distancia)

# Entrenar los modelos con datos balanceados
model_tiempo = RandomForestClassifier(class_weight='balanced', random_state=42)
model_tiempo.fit(X_train_smote, y_train_tiempo_smote)

model_costo = RandomForestClassifier(class_weight='balanced', random_state=42)
model_costo.fit(X_train_smote_costo, y_train_costo_smote)

model_distancia = RandomForestClassifier(class_weight='balanced', random_state=42)
model_distancia.fit(X_train_smote_distancia, y_train_distancia_smote)

# Predicciones
y_pred_tiempo = model_tiempo.predict(X_test_numeric)
y_pred_costo = model_costo.predict(X_test_numeric)
y_pred_distancia = model_distancia.predict(X_test_numeric)

# Evaluar los modelos
print("Evaluación del modelo por tiempo:")
print(classification_report(y_test_tiempo, y_pred_tiempo))

print("\nEvaluación del modelo por costo:")
print(classification_report(y_test_costo, y_pred_costo))

print("\nEvaluación del modelo por distancia:")
print(classification_report(y_test_distancia, y_pred_distancia))
