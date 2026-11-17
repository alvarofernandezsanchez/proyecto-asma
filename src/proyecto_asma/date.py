import pandas as pd
import logging

logger = logging.getLogger(__name__)


def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    try:
        logging.info("Limpiando datos...")
        df_cleaned = df.copy()
        df_cleaned = df.astype(object).where(pd.notna(df), None) #para evitar problemas con los valores nulos al insertar en MySQL, convertimos los NaN a None
        df_cleaned["estado_aut"] = pd.to_datetime(df["estado_aut"], unit="ms", errors="coerce")
        df_cleaned["estado_rev"] = pd.to_datetime(df["estado_rev"], unit="ms", errors="coerce")
        logger.info("Datos limpiados correctamente.")
        return df_cleaned
        
    except Exception as e:
        logger.exception("Error al limpiar datos.")
        raise e

if __name__ == "__main__":
    df = pd.read_csv("datos_completos.csv")
    df_cleaned = clean_data(df)
    df_cleaned.to_csv("datos_completos_limpios.csv", index=False)