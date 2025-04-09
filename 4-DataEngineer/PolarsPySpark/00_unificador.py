from utils import ParquetMerger
from pathlib import Path
from configparser import ConfigParser

# Leer rutas desde config.ini
config = ConfigParser()
config.read(Path(__file__).parent / "utils" / "config.ini")

input_folder = config.get("parquet", "input_folder")
output_file = config.get("parquet", "output_file")

# Convertir a rutas absolutas basadas en cwd
input_path = Path.cwd() / input_folder
output_path = Path.cwd() / output_file

# Ejecutar
merger = ParquetMerger(input_folder=input_path, output_file=output_path)
df = merger.merge()
