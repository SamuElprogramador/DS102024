# Integración del Pipeline ETL en Mage.ai

En esta sección, explicaremos cómo integrar los bloques de extracción, transformación y carga en un pipeline completo de ETL en Mage.ai.

## Estructura del Pipeline

En Mage.ai, un pipeline se compone de bloques interconectados que se ejecutan en secuencia. Para nuestro ejemplo ETL, tendremos:

1. Un bloque de extracción que obtiene datos de ventas
2. Un bloque de transformación que limpia y enriquece los datos
3. Un bloque de carga que almacena los datos en DuckDB

## Creación del Pipeline en Mage.ai

Para crear un pipeline ETL en Mage.ai, sigue estos pasos:

1. Accede a la interfaz web de Mage.ai en http://localhost:6789
2. Haz clic en "New pipeline"
3. Selecciona "Standard (batch)" como tipo de pipeline
4. Asigna un nombre como "ventas_etl_pipeline"
5. Haz clic en "Create pipeline"

## Añadir Bloques al Pipeline

Una vez creado el pipeline, puedes añadir los bloques:

### Bloque de Extracción

1. Haz clic en "Data loader" en el menú de la izquierda
2. Selecciona "Python" como tipo de bloque
3. Copia el código del archivo `etl_example_extract.py`
4. Guarda el bloque con un nombre descriptivo (ej. "extract_sales_data")

### Bloque de Transformación

1. Haz clic en el bloque de extracción
2. Haz clic en "+" para añadir un nuevo bloque
3. Selecciona "Transformer" y luego "Python"
4. Copia el código del archivo `etl_example_transform.py`
5. Guarda el bloque con un nombre descriptivo (ej. "transform_sales_data")

### Bloque de Carga

1. Haz clic en el bloque de transformación
2. Haz clic en "+" para añadir un nuevo bloque
3. Selecciona "Data exporter" y luego "Python"
4. Copia el código del archivo `etl_example_load.py`
5. Guarda el bloque con un nombre descriptivo (ej. "load_sales_data")

## Ejecución del Pipeline

Para ejecutar el pipeline completo:

1. Haz clic en "Run pipeline" en la parte superior derecha
2. Observa el progreso de la ejecución en la pestaña "Runs"
3. Verifica los resultados de cada bloque

## Programación del Pipeline

Para programar la ejecución periódica del pipeline:

1. Ve a la pestaña "Triggers"
2. Haz clic en "Create trigger"
3. Selecciona "Schedule" como tipo de trigger
4. Configura la frecuencia de ejecución (ej. diaria, semanal)
5. Guarda el trigger

## Monitoreo y Observabilidad

Mage.ai proporciona herramientas para monitorear tus pipelines:

1. Ve a la pestaña "Runs" para ver el historial de ejecuciones
2. Haz clic en una ejecución específica para ver detalles
3. Revisa los logs para identificar posibles errores
4. Configura alertas para recibir notificaciones en caso de fallos

Este flujo de trabajo ETL es un ejemplo básico que puedes expandir según tus necesidades específicas, añadiendo más fuentes de datos, transformaciones más complejas o destinos adicionales para los datos procesados.
