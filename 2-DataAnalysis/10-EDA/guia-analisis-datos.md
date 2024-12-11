# Guía Detallada para el Análisis de Datos

## 1. Primera Observación
1. Inspeccionar el tamaño y estructura de los datos
   * Número total de registros
   * Número de columnas
   * Espacio en memoria utilizado
   * Verificar si hay jerarquías o estructuras anidadas

2. Verificar tipos de datos y nombres de columnas
   * Consistencia en el naming (snake_case, camelCase)
   * Tipos de datos apropiados para cada variable
   * Documentación de cada columna y su significado

3. Identificar valores duplicados o errores evidentes
   * Duplicados exactos vs duplicados parciales
   * Errores de codificación (UTF-8, ASCII)
   * Problemas de importación o parsing

## 2. Análisis Exploratorio de Datos (EDA)

### 2.1 Análisis Univariado
1. Variables Numéricas:
   * Estadísticas descriptivas (media, mediana, desviación estándar)
   * Histogramas y density plots
   * Box plots
   * Pruebas de normalidad (Shapiro-Wilk, QQ-plots)

2. Variables Categóricas:
   * Frecuencias absolutas y relativas
   * Gráficos de barras
   * Diagramas de Pareto
   * Análisis de cardinalidad

### 2.2 Análisis Bivariado
1. Relaciones entre variables numéricas:
   * Matrices de correlación
   * Scatter plots
   * Heat maps

2. Relaciones entre variables categóricas:
   * Tablas de contingencia
   * Test Chi-cuadrado
   * Análisis de correspondencia

3. Relaciones numéricas-categóricas:
   * Box plots por grupo
   * Violin plots
   * ANOVA

### 2.3 Tabla Resumen Detallada
* Nombre de la variable
* Tipo de dato (int, float, str...)
* Tipo de variable (numérica, categórica...)
* Cardinalidad
* Distribución (gaussiana, uniforme...)
* Valores faltantes (cantidad y porcentaje)
* Outliers (cantidad y porcentaje)
* Rango de valores
* Moda/Media/Mediana
* Asimetría y Curtosis
* Resultados de pruebas de normalidad

## 3. Tratamiento de Datos

### 3.1 Análisis Detallado de Valores Faltantes
1. Patrones de Missing Data:
   * MCAR (Missing Completely at Random)
     - Test de Little para MCAR
     - Análisis de aleatoriedad en los patrones
     - Comparación de distribuciones entre datos faltantes y no faltantes

   * MAR (Missing at Random)
     - Análisis de correlación entre missingness y otras variables
     - Patrones de missingness condicional
     - Visualización de patrones de missingness

   * MNAR (Missing Not at Random)
     - Identificación de sesgos sistemáticos
     - Análisis de causas de no respuesta
     - Evaluación del impacto en el análisis

2. Estrategias de Imputación:
   * Simples:
     - Media/Mediana/Moda
     - Valores constantes
     - Interpolación lineal

   * Avanzadas:
     - KNN
     - Random Forest
     - Multiple Imputation by Chained Equations (MICE)
     - Expectation-Maximization (EM)

3. Validación de Imputación:
   * Cross-validation de métodos de imputación
   * Análisis de sensibilidad
   * Comparación de distribuciones pre/post imputación

### 3.2 Tratamiento de Outliers
1. Métodos de Detección:
   * Estadísticos:
     - Z-score
     - IQR (Rango Intercuartílico)
     - Test de Grubbs
     - Test de Dixon

   * Machine Learning:
     - Isolation Forest
     - Local Outlier Factor
     - DBSCAN

2. Estrategias de Tratamiento:
   * Winsorización
   * Transformaciones (log, raíz cuadrada)
   * Eliminación justificada
   * Creación de categorías específicas

## 4. Análisis Descriptivo
1. Estadísticas Descriptivas:
   * Medidas de tendencia central
   * Medidas de dispersión
   * Medidas de forma
   * Análisis de percentiles

2. Visualizaciones:
   * Series temporales
   * Gráficos de composición
   * Diagramas de dispersión matriciales
   * Mapas de calor interactivos

## 5. Análisis Diagnóstico
1. Análisis de Relaciones:
   * Análisis de componentes principales (PCA)
   * Análisis factorial
   * Clustering exploratorio

2. Pruebas Estadísticas:
   * Paramétricas vs No paramétricas
   * Tests de independencia
   * Análisis de varianza multivariado

## 6. Análisis Inferencial
1. Pruebas de Hipótesis:
   * Definición de hipótesis nula y alternativa
   * Selección del nivel de significancia
   * Cálculo de poder estadístico

2. Modelado Estadístico:
   * Regresión lineal/logística
   * Modelos mixtos
   * Series temporales

## 7. Análisis Predictivo
1. Preparación:
   * Feature engineering
   * Selección de variables
   * Validación cruzada

2. Modelado:
   * Árboles de decisión
   * Random Forest
   * Gradient Boosting
   * Redes neuronales

## 8. Análisis Prescriptivo
1. Optimización:
   * Programación lineal
   * Optimización de hiperparámetros
   * Análisis de escenarios

## 9. Análisis Causal
1. Diseño Experimental:
   * A/B testing
   * Diseño factorial
   * Análisis de mediación

2. Inferencia Causal:
   * Modelos de ecuaciones estructurales
   * Propensity score matching
   * Análisis de intervención
