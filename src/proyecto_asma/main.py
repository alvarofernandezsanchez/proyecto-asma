from proyecto_asma.hu1 import get_datos
from proyecto_asma.hu2 import add_metricas
from proyecto_asma.hu3 import add_variables_nomenclator
import pandas as pd
from sklearn.cluster import KMeans
from proyecto_asma.database import connect_to_database, insert_sql
from proyecto_asma.date import clean_data

import logging

logging.basicConfig(level=logging.INFO)

def get_datos_completos(enfermedad) -> pd.DataFrame:
    print("HU1...")
    df_hu1 = get_datos(enfermedad)
    print("HU2...")
    df_hu2 = add_metricas(df_hu1)
    print("HU3...")
    df_hu3 = add_variables_nomenclator(df_hu2)  
    return df_hu3

def preparar_clustering(df: pd.DataFrame) -> pd.DataFrame:
    new_df = df.copy()
    numerical_columns = ['pvp_iva', 'n_graves', 'n_tablas', 'n_palabras', 'num_principios_activos']
    new_df = new_df[numerical_columns]
    new_df["pvp_iva"] = new_df["pvp_iva"].fillna(new_df["pvp_iva"].mean())
    
    return new_df

def clean(df: pd.DataFrame) -> pd.DataFrame:
    df_cleaned = df.astype(object).where(pd.notna(df), None)
    df_cleaned = clean_data(df_cleaned)
    return df_cleaned
    
def clustering(df: pd.DataFrame, n_clusters: int = 3) -> pd.DataFrame:
    df_cleaned = preparar_clustering(df)
    kmeans = KMeans(n_clusters=n_clusters, random_state=42)
    df['cluster'] = kmeans.fit_predict(df_cleaned)
    return df

def sql_insert(df: pd.DataFrame):
    conexion, cursor = connect_to_database()
    insert_sql(conexion, cursor, df)
    
def pipeline(enfermedad: str, n_clusters: int = 3, loaded: bool = True):
    if not loaded:
        df_completo = get_datos_completos(enfermedad)
    else:
        df_completo = pd.read_csv("datos_completos.csv")
    df_cleaned = clean_data(df_completo)
    df_clustered = clustering(df_cleaned, n_clusters=3)
    sql_insert(df_clustered)
    
    
if __name__ == "__main__":
    enfermedad = "asma"
    pipeline(enfermedad)
    
