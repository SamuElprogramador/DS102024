# Notebook de Ejemplo: ELT con Mage.ai

Este notebook explicativo muestra cómo implementar un proceso ELT (Extract, Load, Transform) utilizando Mage.ai. Aprenderemos los conceptos básicos y crearemos un pipeline ELT completo.

## ¿Qué es ELT?

ELT (Extract, Load, Transform) es un proceso que consiste en:

1. **Extracción (Extract)**: Obtener datos de diversas fuentes (APIs, bases de datos, archivos, etc.)
2. **Carga (Load)**: Almacenar los datos sin procesar en el destino (data warehouse, data lake, etc.)
3. **Transformación (Transform)**: Transformar los datos directamente en el destino utilizando las capacidades de procesamiento del sistema de destino

## ELT vs ETL: Diferencias Clave

| Característica | ETL | ELT |
|----------------|-----|-----|
| Orden de operaciones | Transformar antes de cargar | Transformar después de cargar |
| Ubicación de transformación | En memoria o servidor intermedio | En el sistema de destino |
| Escalabilidad | Limitada por recursos del servidor ETL | Aprovecha la potencia del data warehouse |
| Flexibilidad | Requiere rediseño para nuevas transformaciones | Permite transformaciones ad-hoc sobre datos ya cargados |
| Casos de uso ideales | Datos estructurados, volúmenes moderados | Big data, análisis exploratorio, datos no estructurados |

## Estructura del Pipeline ELT en Mage.ai

En Mage.ai, un pipeline ELT se compone de bloques interconectados:

1. **Bloque de Extracción**: Utiliza decoradores `@data_loader` para obtener datos
2. **Bloque de Carga**: Utiliza decoradores `@data_exporter` para almacenar datos sin procesar
3. **Bloque de Transformación**: Utiliza SQL u otros métodos para transformar datos directamente en el destino

Vamos a crear un ejemplo práctico de ELT utilizando datos de ventas de una tienda online.
