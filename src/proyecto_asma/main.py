from hu1 import get_datos
from hu2 import add_metricas
from hu3 import add_variables_nomenclator
import pandas as pd

def get_datos_completos(enfermedad) -> pd.DataFrame:
    print("HU1...")
    df_hu1 = get_datos(enfermedad)
    print("HU2...")
    df_hu2 = add_metricas(df_hu1)
    print("HU3...")
    df_hu3 = add_variables_nomenclator(df_hu2)    
    return df_hu3

if __name__ == "__main__":
    df = get_datos_completos("asma")
    df.to_csv("datos_completos.csv", index=False)
    df.to_excel("datos_completos.xlsx", index=False)
    print("Datos generados correctamente")
    print(df.info())
    