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
    response = requests.get(URL)
    response.raise_for_status()
    df = pd.read_excel(io.BytesIO(response.content), engine="xlrd") #este engine sirve para que excels mas antiguos se puedan leer con pandas
    return df

def cocinar_nomenclator(df_nomenclator: pd.DataFrame) -> pd.DataFrame: #lo dejamos preparado
    df  = df_nomenclator[COLUMNAS].copy()
    df = df.rename(columns={
        "Código Nacional" : "cn",
        "Estado" : "estado_nomenclator",
        "Precio de venta al público con IVA" : "pvp_iva",
        "Precio de referencia" : "precio_referencia",
        "Tratamiento de larga duración" : "tratamiento_larga_duracion",
        "Especial control médico" : "especial_control_medico",
    })

    df["cn"] = df["cn"].astype(str).str.strip().str.replace(r"\.0$", "", regex=True) #(linea metida con ia), con esto nos aseguramos de que la conversion se haga bien = el merge no falle
    return df

if __name__ == "__main__":
    df_medicamentos = pd.read_excel("datos_finales.xlsx")
    df_medicamentos["cn"] = df_medicamentos["cn"].astype(str).str.strip().str.replace(r"\.0$", "", regex=True)


    df_nomenclator = descargar_nomenclator()

    #print(df_nomenclator.columns.tolist()) #verificamos que las 6 columnas estan ok

    df_nomenclator_amoldado = cocinar_nomenclator(df_nomenclator)
    df_final = df_medicamentos.merge(df_nomenclator_amoldado)

    print(df_final.head())
    print(f"Medicamentos sin cruce en el nomenclator: {df_final['pvp_iva'].isna().sum()}")

    df_final.to_excel("datos_final_pro.xlsx", index=False)
    df_final.to_csv("datos_final_pro.csv", index=False) #metemos index=false para evitar que se meta una columna mas y se guarde limpito