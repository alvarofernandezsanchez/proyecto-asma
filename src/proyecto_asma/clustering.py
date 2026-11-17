import logging
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import silhouette_score

logger = logging.getLogger(__name__)

def preparar_clustering(df: pd.DataFrame) -> pd.DataFrame:
    new_df = df.copy()
    numerical_columns = ['pvp_iva', 'n_graves', 'n_tablas', 'n_palabras', 'num_principios_activos']
    new_df = new_df[numerical_columns]
    new_df["pvp_iva"] = new_df["pvp_iva"].fillna(new_df["pvp_iva"].mean())
    X = new_df.values
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    new_df = pd.DataFrame(X_scaled, columns=numerical_columns)
    return new_df
    
def clustering(df: pd.DataFrame, n_clusters: int = 3) -> pd.DataFrame:
    logger.info("Realizando clustering con %d clusters sobre %d filas.", n_clusters, len(df))
    df_cleaned = preparar_clustering(df)
    kmeans = KMeans(n_clusters=n_clusters, random_state=42)
    df['cluster'] = kmeans.fit_predict(df_cleaned)
    silhouette = silhouette_score(df_cleaned, df['cluster'])
    logger.info(f"Clustering completado. Silhouette: {silhouette:.2f}.")
    return df
    
    
if __name__ == "__main__":
    df = pd.read_csv("datos_completos.csv")
    df_clustered = clustering(df, n_clusters=3)
    df_clustered.to_csv("datos_completos_clusters.csv", index=False)
    