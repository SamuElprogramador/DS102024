import logging
import polars as pl
from pathlib import Path

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)

class ParquetMerger:
    def __init__(self, input_folder: Path, output_file: Path):
        self.input_folder = input_folder
        self.output_file = output_file

    def _get_parquet_files(self) -> list[Path]:
        archivos = sorted(self.input_folder.glob("*.parquet"))
        logging.info(f"Archivos encontrados: {[f.name for f in archivos]}")
        return archivos

    def merge(self) -> pl.DataFrame:
        archivos = self._get_parquet_files()
        if not archivos:
            raise FileNotFoundError(f"No se encontraron archivos .parquet en {self.input_folder.resolve()}")

        logging.info(f"Unificando {len(archivos)} archivos parquet...")

        dataframes = []
        for archivo in archivos:
            df = pl.read_parquet(archivo)
            # Normalizar columnas datetime a la misma resolución
            for col in df.columns:
                if df[col].dtype == pl.Datetime("us") or df[col].dtype == pl.Datetime("ms") or df[col].dtype == pl.Datetime("ns"):
                    df = df.with_columns(
                        df[col].cast(pl.Datetime("ns"))
                    )
            dataframes.append(df)

        df_final = pl.concat(dataframes)
        self.output_file.parent.mkdir(parents=True, exist_ok=True)
        df_final.write_parquet(self.output_file)
        logging.info(f"Archivo unificado guardado en: {self.output_file}")
        return df_final
