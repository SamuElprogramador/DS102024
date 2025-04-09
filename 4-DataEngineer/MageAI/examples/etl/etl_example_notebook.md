# Notebook de Ejemplo: ETL con Mage.ai

Este notebook explicativo muestra cómo implementar un proceso ETL (Extract, Transform, Load) utilizando Mage.ai. Aprenderemos los conceptos básicos y crearemos un pipeline ETL completo.

## ¿Qué es ETL?

ETL (Extract, Transform, Load) es un proceso que consiste en:

1. **Extracción (Extract)**: Obtener datos de diversas fuentes (APIs, bases de datos, archivos, etc.)
2. **Transformación (Transform)**: Limpiar, enriquecer y transformar los datos para que sean útiles
3. **Carga (Load)**: Almacenar los datos transformados en un destino (data warehouse, data lake, etc.)

En un proceso ETL tradicional, los datos se transforman antes de cargarlos en el destino final.

## Estructura del Pipeline ETL en Mage.ai

En Mage.ai, un pipeline ETL se compone de bloques interconectados:

1. **Bloque de Extracción**: Utiliza decoradores `@data_loader` para obtener datos
2. **Bloque de Transformación**: Utiliza decoradores `@transformer` para procesar datos
3. **Bloque de Carga**: Utiliza decoradores `@data_exporter` para almacenar datos

Vamos a crear un ejemplo práctico de ETL utilizando datos de ventas de una tienda online.
