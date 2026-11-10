from hu1 import get_datos
from hu2 import add_metricas
from hu3 import add_variables_nomenclator
import pandas as pd
from sklearn.cluster import KMeans
from database import connect_to_database, insert_sql


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
    categorical_columns = ["formaFarmaceuticaSimplificada", "tratamiento_larga_duracion", "estado_nomenclator", "biosimilar", "triangulo", "conduc", "generico", "comerc", "viasAdministracion"] 
    drop_columns =['nregistro', 'nombre', 'cn', 'url_foto_materiales', 'url_html_ficha_tecnica', 'estado_rev', 'estado_aut', 'labtitular', 'pactivos', 'num_registros_atc', 'especial_control_medico', 'huerfano', 'receta', 'dosis', 'precio_referencia']
    new_df = new_df[numerical_columns]
    new_df["pvp_iva"] = new_df["pvp_iva"].fillna(new_df["pvp_iva"].mean())
    
    return new_df

def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    df_cleaned = df.copy()
    df_cleaned["estado_aut"] = pd.to_datetime(df["estado_aut"], errors='coerce')
    df_cleaned["estado_rev"] = pd.to_datetime(df["estado_rev"], errors='coerce')
    df_cleaned = df.astype(object).where(pd.notna(df), None)
    
    return df_cleaned
    
def clustering(df: pd.DataFrame, n_clusters: int = 3) -> pd.DataFrame:
    kmeans = KMeans(n_clusters=n_clusters, random_state=42)
    df['cluster'] = kmeans.fit_predict(df)
    return df

def sql_insert(df: pd.DataFrame):
    conexion, cursor = connect_to_database()
    insert_sql(conexion, cursor, df)
    

if __name__ == "__main__":
    enfermedad = "asma"
    df_completo = get_datos_completos(enfermedad)
    df_cleaned = clean_data(df_completo)
    df_prepared = preparar_clustering(df_cleaned)
    df_clustered = clustering(df_prepared, n_clusters=3)
    sql_insert(df_clustered)
    
