from proyecto_asma.hu1 import get_datos
from proyecto_asma.hu2 import add_metricas
from proyecto_asma.hu3 import add_variables_nomenclator
import pandas as pd
from proyecto_asma.clustering import clustering
from proyecto_asma.database import connect_to_database, insert_sql
from proyecto_asma.date import clean_data

import logging

logging.basicConfig(level=logging.INFO)


def get_datos_completos(enfermedad) -> pd.DataFrame:
    try:
        if enfermedad == None:
            logging.warning("No se ha especificado una enfermedad. Se utilizará 'asma' por defecto.")
            enfermedad = "asma"
        logging.info("Cargando datos de HU1...")
        df_hu1 = get_datos(enfermedad)
        logging.info("HU1 completada: %d filas, %d columnas.", *df_hu1.shape)
        logging.info("Cargando datos de HU2...")
        df_hu2 = add_metricas(df_hu1)
        logging.info("HU2 completada: %d filas, %d columnas.", *df_hu2.shape)
        logging.info("Cargando datos de HU3...")
        df_hu3 = add_variables_nomenclator(df_hu2) 
        logging.info("HU3 completada: %d filas, %d columnas.", *df_hu3.shape)
        return df_hu3
    except Exception as e:
        logging.exception("Error al cargar datos completos.")
        raise
    
def sql_insert(df: pd.DataFrame):
    logging.info(f"Preparando inserción en MySQL de {len(df)} filas.")
    conexion, cursor = connect_to_database()
    insert_sql(conexion, cursor, df)
    
def pipeline(enfermedad: str, n_clusters: int = 3, loaded: bool = True):
    logging.info(f"Iniciando pipeline. Enfermedad: {enfermedad}, clusters: {n_clusters}, datos cargados: {loaded}.")
    if not loaded:
        df_completo = get_datos_completos(enfermedad)
    else:
        logging.info("Usando datos cargados previamente.")
        df_completo = pd.read_csv("datos_completos.csv")
    df_cleaned = clean_data(df_completo)
    df_clustered = clustering(df_cleaned, n_clusters=n_clusters)
    sql_insert(df_clustered)
    logging.info("Pipeline completado correctamente.")
    
    
if __name__ == "__main__":
    enfermedad = "asma"
    pipeline(enfermedad)
    
