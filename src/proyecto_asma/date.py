import pandas as pd

df = pd.read_csv("datos_completos_clusters.csv")

df["estado_aut"] = pd.to_datetime(df["estado_aut"], errors='coerce')
df["estado_rev"] = pd.to_datetime(df["estado_rev"], errors='coerce')

df.to_csv("datos_completos_clusters.csv", index=False)