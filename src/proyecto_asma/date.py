import pandas as pd

df = pd.read_csv("datos_completos_clusters.csv")
def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    df_cleaned = df.copy()
    df_cleaned["estado_aut"] = pd.to_datetime(df["estado_aut"], unit="ms", errors="coerce")
    df_cleaned["estado_rev"] = pd.to_datetime(df["estado_rev"], unit="ms", errors="coerce")
    return df_cleaned

print(df["estado_aut"])
df.to_csv("datos_completos_clusters.csv", index=False)