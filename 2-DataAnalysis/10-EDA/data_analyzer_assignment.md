# 🎯 Proyecto: Creación de una Clase de Análisis de Datos

## 📝 Descripción
Desarrollar una clase en Python llamada `DataAnalyzer` que permita realizar análisis exploratorio y visualización de datos de manera eficiente y visualmente atractiva.

## 🎯 Objetivos
- Implementar métodos para análisis exploratorio de datos
- Crear visualizaciones informativas y estéticas
- Practicar programación orientada a objetos
- Desarrollar documentación clara y profesional

## 📋 Requisitos
La clase debe implementar los siguientes métodos:

### 1. Métodos Básicos de Exploración
```python
def load_data(self, path: str) -> None:
    """Carga los datos desde un archivo CSV/Excel"""

def get_info(self) -> dict:
    """Retorna información básica del dataset:
    - Dimensiones
    - Tipos de datos
    - Memoria utilizada
    - Resumen estadístico básico
    """
```

### 2. Métodos de Análisis Estadístico
```python
def describe_numeric(self) -> pd.DataFrame:
    """Análisis estadístico detallado de variables numéricas:
    - Media, mediana, moda
    - Desviación estándar
    - Cuartiles
    - Asimetría y curtosis
    """

def describe_categorical(self) -> pd.DataFrame:
    """Análisis de variables categóricas:
    - Frecuencias
    - Proporciones
    - Valores únicos
    """
```

### 3. Métodos de Visualización
```python
def plot_distribution(self, column: str) -> None:
    """Genera gráficos de distribución:
    - Histogramas para numéricas
    - Gráficos de barras para categóricas
    """

def plot_correlation_matrix(self) -> None:
    """Crea un heatmap de correlaciones"""

def plot_boxplots(self) -> None:
    """Genera boxplots para variables numéricas"""
```

### 4. Métodos de Limpieza
```python
def handle_missing_values(self, strategy: str = 'mean') -> None:
    """Maneja valores faltantes con diferentes estrategias"""

def remove_outliers(self, method: str = 'iqr') -> None:
    """Detecta y maneja outliers"""
```

### 5. Métodos de Transformación
```python
def normalize_data(self, columns: list) -> None:
    """Normaliza variables numéricas"""

def encode_categorical(self, columns: list) -> None:
    """Codifica variables categóricas"""
```

## 📊 Ejemplo de Uso Esperado
```python
# Inicializar el analizador
analyzer = DataAnalyzer()

# Cargar datos
analyzer.load_data('datos.csv')

# Obtener información básica
info = analyzer.get_info()

# Generar visualizaciones
analyzer.plot_distribution('edad')
analyzer.plot_correlation_matrix()

# Limpiar datos
analyzer.handle_missing_values()
analyzer.remove_outliers()
```

## 🌟 Bonus (Funcionalidades Adicionales)
- Exportación de reportes en HTML/PDF
- Detección automática de tipos de variables
- Sugerencias de visualizaciones según el tipo de dato