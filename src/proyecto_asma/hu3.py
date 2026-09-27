import requests
import pandas as pd
import io

URL = "https://www.sanidad.gob.es/profesionales/nomenclator.do?metodo=nomenclatorExcel"

COLUMNAS = [
    "Código Nacional",
    "Estado",
    "Precio de venta al público con IVA",
    "Precio de referencia",
    "Tratamiento de larga duración",
    "Especial control médico",
]

def descargar_nomenclator() -> pd.DataFrame:
    # obtenemos el nomenclátor y lo guardamos en un Dataframe
    response = requests.get(URL)
    response.raise_for_status()
    df = pd.read_excel(io.BytesIO(response.content))
    return df

def cocinar_nomenclator(df_nomenclator: pd.DataFrame) -> pd.DataFrame: #lo dejamos preparado
    df  = df_nomenclator[COLUMNAS].copy()
    # modificamos el nombre de las columnas, principalmente de Codigo nacional para que coincida con el "cn" del Dataframe original
    df = df.rename(columns={
        "Código Nacional" : "cn",
        "Estado" : "estado_nomenclator",
        "Precio de venta al público con IVA" : "pvp_iva",
        "Precio de referencia" : "precio_referencia",
        "Tratamiento de larga duración" : "tratamiento_larga_duracion",
        "Especial control médico" : "especial_control_medico",
    })
    return df


# Función que automatiza todo HU3
def add_variables_nomenclator(df: pd.DataFrame) -> pd.DataFrame:
    df_nomenclator = descargar_nomenclator()
    df_nomenclator_amoldado = cocinar_nomenclator(df_nomenclator)
    
    #(lineas metida con ia), con esto nos aseguramos de que la conversion se haga bien = el merge no falle
    df["cn"] = df["cn"].astype(str).str.strip().str.replace(r"\.0$", "", regex=True)
    df_nomenclator_amoldado["cn"] = df_nomenclator_amoldado["cn"].astype(str).str.strip().str.replace(r"\.0$", "", regex=True) 
    
    # Hacemos un merge de tipo left join en cn. Así evitamos eliminar medicamentos que no aparezcan en el nomenclator
    df_final = df.merge(df_nomenclator_amoldado, on="cn", how="left")
    return df_final


if __name__ == "__main__":
    df_medicamentos = pd.read_excel("datos_finales.xlsx")
    df_nomenclator = descargar_nomenclator()

    #print(df_nomenclator.columns.tolist()) #verificamos que las 6 columnas estan ok

    df_nomenclator_amoldado = cocinar_nomenclator(df_nomenclator)
    df_final = df_medicamentos.merge(df_nomenclator_amoldado, on="cn", how="left")
    print(f"Medicamentos sin cruce en el nomenclator: {df_final['pvp_iva'].isna().sum()}")

    df_final.to_excel("datos_final_pro.xlsx", index=False)
    df_final.to_csv("datos_final_pro.csv", index=False) #metemos index=false para evitar que se meta una columna mas y se guarde limpito