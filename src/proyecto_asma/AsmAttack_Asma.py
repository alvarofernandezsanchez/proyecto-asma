import pandas as pd
import logging
from datetime import datetime
from proyecto_asma.hu1 import get_datos
from proyecto_asma.hu2 import add_metricas
from proyecto_asma.hu3 import add_variables_nomenclator
from proyecto_asma.clustering import clustering
from proyecto_asma.database import connect_to_database, insert_sql
from proyecto_asma.date import clean_data

enfermedad_log = "asma"
fecha_log = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
nombre_log = f"AsmAttack_{enfermedad_log}_{fecha_log}.log"

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
    handlers=[logging.FileHandler(nombre_log, encoding="utf-8")],
)
logger = logging.getLogger(__name__)


def get_datos_completos(enfermedad) -> pd.DataFrame:
    try:
        if enfermedad == None:
            logger.warning("No se ha especificado una enfermedad. Se utilizará 'asma' por defecto.")
            enfermedad = "asma"
        logger.info("Cargando datos de HU1...")
        df_hu1 = get_datos(enfermedad)
        logger.info("HU1 completada: %d filas, %d columnas.", *df_hu1.shape)
        logger.info("Cargando datos de HU2...")
        df_hu2 = add_metricas(df_hu1)
        logger.info("HU2 completada: %d filas, %d columnas.", *df_hu2.shape)
        logger.info("Cargando datos de HU3...")
        df_hu3 = add_variables_nomenclator(df_hu2) 
        logger.info("HU3 completada: %d filas, %d columnas.", *df_hu3.shape)
        return df_hu3
    except Exception as e:
        logger.exception("Error al cargar datos completos.")
        raise
    
def sql_insert(df: pd.DataFrame):
    logger.info("Preparando inserción en MySQL de %d filas.", len(df))
    conexion, cursor = connect_to_database()
    insert_sql(conexion, cursor, df)
    
def pipeline(enfermedad: str, n_clusters: int = 3, loaded: bool = True):
    logger.info("Iniciando pipeline. Enfermedad: %s, clusters: %d, datos cargados: %s.", enfermedad, n_clusters, loaded)
    if not loaded:
        df_completo = get_datos_completos(enfermedad)
    else:
        logger.info("Usando datos cargados previamente.")
        df_completo = pd.read_csv("datos_completos.csv")
    df_cleaned = clean_data(df_completo)
    df_clustered = clustering(df_cleaned, n_clusters=n_clusters)
    sql_insert(df_clustered)
    logger.info("Pipeline completado correctamente.")
    
    
if __name__ == "__main__":
    enfermedad = "asma"
    pipeline(enfermedad)
    
