# Integración del Pipeline ELT en Mage.ai

En esta sección, explicaremos cómo integrar los bloques de extracción, carga y transformación en un pipeline completo de ELT en Mage.ai.

## Estructura del Pipeline ELT

En Mage.ai, un pipeline ELT se compone de bloques interconectados que se ejecutan en secuencia. Para nuestro ejemplo ELT, tendremos:

1. Un bloque de extracción que obtiene datos de ventas
2. Un bloque de carga que almacena los datos sin procesar en DuckDB
3. Un bloque de transformación que procesa los datos directamente en DuckDB

## Creación del Pipeline en Mage.ai

Para crear un pipeline ELT en Mage.ai, sigue estos pasos:

1. Accede a la interfaz web de Mage.ai en http://localhost:6789
2. Haz clic en "New pipeline"
3. Selecciona "Standard (batch)" como tipo de pipeline
4. Asigna un nombre como "ventas_elt_pipeline"
5. Haz clic en "Create pipeline"

## Añadir Bloques al Pipeline

Una vez creado el pipeline, puedes añadir los bloques:

### Bloque de Extracción

1. Haz clic en "Data loader" en el menú de la izquierda
2. Selecciona "Python" como tipo de bloque
3. Copia el código del archivo `elt_example_extract.py`
4. Guarda el bloque con un nombre descriptivo (ej. "extract_sales_data_for_elt")

### Bloque de Carga

1. Haz clic en el bloque de extracción
2. Haz clic en "+" para añadir un nuevo bloque
3. Selecciona "Data exporter" y luego "Python"
4. Copia el código del archivo `elt_example_load.py`
5. Guarda el bloque con un nombre descriptivo (ej. "load_raw_sales_data")

### Bloque de Transformación

1. Haz clic en el bloque de carga
2. Haz clic en "+" para añadir un nuevo bloque
3. Selecciona "Data loader" y luego "Python" (usamos data loader porque devuelve datos)
4. Copia el código del archivo `elt_example_transform.py`
5. Guarda el bloque con un nombre descriptivo (ej. "transform_data_in_database")

## Diferencias Clave con ETL

Observa las diferencias clave entre este pipeline ELT y el pipeline ETL que creamos anteriormente:

1. **Orden de operaciones**: En ELT, cargamos los datos sin procesar antes de transformarlos, mientras que en ETL transformamos los datos antes de cargarlos.

2. **Ubicación de transformación**: En ELT, las transformaciones se realizan directamente en la base de datos (DuckDB), aprovechando su potencia de procesamiento, mientras que en ETL las transformaciones se realizan en memoria.

3. **Complejidad de transformaciones**: En ELT, podemos realizar transformaciones más complejas utilizando SQL directamente en la base de datos, como crear modelos dimensionales (tablas de hechos y dimensiones).

4. **Flexibilidad**: En ELT, podemos crear múltiples transformaciones sobre los mismos datos sin necesidad de volver a extraerlos, lo que proporciona mayor flexibilidad para el análisis exploratorio.

## Ejecución del Pipeline

Para ejecutar el pipeline completo:

1. Haz clic en "Run pipeline" en la parte superior derecha
2. Observa el progreso de la ejecución en la pestaña "Runs"
3. Verifica los resultados de cada bloque

## Ventajas del Enfoque ELT

El enfoque ELT ofrece varias ventajas:

1. **Escalabilidad**: Aprovecha la potencia de procesamiento del sistema de destino, lo que permite manejar grandes volúmenes de datos.

2. **Flexibilidad**: Permite realizar transformaciones ad-hoc sobre los datos ya cargados, sin necesidad de modificar el pipeline de extracción.

3. **Separación de responsabilidades**: Separa claramente las fases de movimiento de datos (extract-load) y procesamiento (transform), lo que facilita la gestión y el mantenimiento.

4. **Preservación de datos sin procesar**: Mantiene una copia de los datos sin procesar, lo que permite realizar nuevas transformaciones en el futuro sin necesidad de volver a extraer los datos.

## Casos de Uso Ideales para ELT

El enfoque ELT es ideal para:

1. **Big data**: Cuando se manejan grandes volúmenes de datos que serían difíciles de procesar en memoria.

2. **Análisis exploratorio**: Cuando se necesita flexibilidad para realizar diferentes tipos de análisis sobre los mismos datos.

3. **Datos no estructurados o semiestructurados**: Cuando la estructura de los datos no está bien definida y se necesita explorarlos antes de decidir cómo transformarlos.

4. **Data warehousing moderno**: Cuando se utilizan sistemas como Snowflake, BigQuery o Redshift que están optimizados para realizar transformaciones a gran escala.

Este flujo de trabajo ELT es un ejemplo básico que puedes expandir según tus necesidades específicas, añadiendo más fuentes de datos, transformaciones más complejas o destinos adicionales para los datos procesados.
