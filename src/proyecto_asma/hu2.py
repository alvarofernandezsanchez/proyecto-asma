import pandas as pd
from bs4 import BeautifulSoup
import re
import requests

def get_n_palabras(response):
    soup = BeautifulSoup(response.text, "html.parser")
    
    h2 = soup.find_all("h2") #buscamos todos los <h2> ya que es el titulo de la sección
    
    for h in h2:
        if h.get_text(strip=True).startswith("4.4"): #si el titulo empieza por 4.4, la guardamos
            seccion_44 = h
            break
    div_44 = seccion_44.find_next("div") # guardamos el siguiente <div>. Este contiene todo el texto de la seccion
    texto = div_44.get_text(" ", strip=True) #pongo " " para separar cada <p> con un espacio y contar palabras bien
    
    return len(texto.split())
    
def get_n_tablas(response):
    soup = BeautifulSoup(response.text, "html.parser")
    tablas = soup.find_all("table") # buscamos todas las etiquetas <table>
    
    return len(tablas)

def get_n_graves(response):
    soup = BeautifulSoup(response.text, "html.parser")
    texto_completo = soup.get_text(" ", strip=True).lower() #cogemos el texto completo de toda la pagina, no hace falta filtrar
    
    # no hago un count("grave") porque puede incluir palabras como "gravedad"
    # usamos expresion regular para identificar todos los "grave" y "graves" siga lo que siga despues (como signos de puntuacion)
    return len(re.findall(r'\bgraves?\b', texto_completo))


# Función que recoge las 3 nuevas métricas
def get_metricas(urls): 
    
    n_palabras = []
    n_tablas = []
    n_grave = []
    #para cada url valida, pasamos la respuesta a cada funcion para calcular cada métrica
    for url in urls:
        response = requests.get(url)
        if response.status_code != 200:
            print(f"Fallo en {url}")
            n_palabras.append(None)
            n_tablas.append(None)
            n_grave.append(None)
            continue
        n_palabras.append(get_n_palabras(response))
        n_tablas.append(get_n_tablas(response))
        n_grave.append(get_n_graves(response))
    
    return n_palabras, n_tablas, n_grave


# Función que automatiza todo el HU2 y añade la información al Dataframe
def add_metricas(df: pd.DataFrame) -> pd.DataFrame:
    urls = df["url_html_ficha_tecnica"]
    n_palabras, n_tablas, n_grave = get_metricas(urls)
    df_metricas = pd.DataFrame({
        "n_palabras": n_palabras,
        "n_tablas": n_tablas,
        "n_graves": n_grave
    })
    df_final = pd.concat([df, df_metricas], axis=1)
    return df_final




      
if __name__ == "__main__":
    df = pd.read_excel("datos.xlsx")
    urls = df["url_html_ficha_tecnica"]
    n_palabras, n_tablas, n_grave = get_metricas(urls)
    
    df_metricas = pd.DataFrame({
        "n_palabras": n_palabras,
        "n_tablas": n_tablas,
        "n_graves": n_grave
    })
    df_final = pd.concat([df, df_metricas], axis=1)
    print(df_final.head())
    
    df_final.to_excel("datos_finales.xlsx", index=False)
    df_final.to_csv("datos_finales.csv", index=False)
    
    