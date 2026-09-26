import requests
import json
import pandas as pd


def get_paginas(enfermedad: str) -> list:
    i = 1
    datos = []

    while True:
        url = f"https://cima.aemps.es/cima/rest/buscarEnFichaTecnica?pagina={i}"

        payload = json.dumps([
            {
              "seccion": "4.1",
              "texto": enfermedad,
              "contiene": 1
            }
        ])
        headers = {
            'Cookie': 'JSESSIONID=3L_KS-QHSOXgqJxYXyuBkUmdehmhvQ-Ub2Qbq44VFy3xy_2iRkNH!962100432',
            'Content-Type': 'application/json'
        }

        response = requests.request("POST", url, headers=headers, data=payload)
        data = response.json()

        if data["totalFilas"] == 0:
            break

        i += 1
        datos.append(data)
    return datos


def get_registros(datos: list) -> pd.DataFrame:
    nregistros = []
    for pagina in datos:
        resultados = pagina["resultados"]
        for resultado in resultados:
            nregistros.append(resultado["nregistro"])

    registros_registrados = []
    for nregistro in nregistros:
        url = f"https://cima.aemps.es/cima/rest/medicamento?nregistro={nregistro}"

        payload = ""
        headers = {
            'Cookie': 'JSESSIONID=3L_KS-QHSOXgqJxYXyuBkUmdehmhvQ-Ub2Qbq44VFy3xy_2iRkNH!962100432'
        }

        response = requests.request("GET", url, headers=headers, data=payload)
        data = response.json()

        data["cn"] = data["presentaciones"][0].get("cn")
        data["estado_aut"] = data["estado"].get("aut")
        data["estado_rev"] = data["estado"].get("rev", None)
        data["url_html_ficha_tecnica"] = data["docs"][0].get("urlHtml")
        url_foto = data.get("fotos", None)
        if url_foto != None: # hacemos esto por que hay algunos que no tienen el campo fotos
            data["url_foto_materiales"] = url_foto[0].get("url", None)
        else:
            data["url_foto_materiales"] = None
        data["formaFarmaceuticaSimplificada"] = data["formaFarmaceuticaSimplificada"].get("nombre")
        data["viasAdministracion"] = data["viasAdministracion"][0].get("nombre")
        data["num_registros_atc"] = len(data["atcs"])
        data["num_principios_activos"] = len(data["principiosActivos"])


        registros_registrados.append(data)

    df = pd.DataFrame(registros_registrados)
    return df


if __name__ == "__main__":
    columnas_validas = [
        "nregistro",
        "nombre",
        "pactivos",
        "labtitular",
        "labcomercializador",
        "cn",
        "dosis",
        "formaFarmaceuticaSimplificada",
        "estado_aut",
        "estado_rev",
        "viasAdministracion",
        "comerc",
        "receta",
        "generico",
        "conduc",
        "triangulo",
        "huerfano",
        "biosimilar",
        "url_html_ficha_tecnica",
        "url_foto_materiales",
        "num_registros_atc",
        "num_principios_activos",
    ]

    datos = get_paginas("asma")
    df = get_registros(datos)
    df_valido = df[columnas_validas]

    df_valido.to_excel("datos.xlsx", index=False)
    df_valido.to_csv("datos.csv", index=False)
    
