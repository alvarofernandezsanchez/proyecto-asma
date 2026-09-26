import pandas as pd
from bs4 import BeautifulSoup
import requests

def get_n_palabras(response):
    soup = BeautifulSoup(response.text, "html.parser")
    
    h2 = soup.find_all("h2")
    
    for h in h2:
        if h.get_text(strip=True).startswith("4.4"):
            seccion_44 = h
            break
    div_44 = seccion_44.find_next("div")
    texto = div_44.get_text(" ", strip=True) #pongo " " para separar cada <p> con un espacio y contar palabras bien
    
    return len(texto.split())
    
def get_n_tablas(response):
    soup = BeautifulSoup(response.text, "html.parser")
    tablas = soup.find_all("table")
    
    return len(tablas)

def get_n_graves(response):
    soup = BeautifulSoup(response.text, "html.parser")
    texto_completo = soup.get_text(" ", strip=True) #cogemos el texto completo de toda la pagina, no hace falta filtrar
    palabras = texto_completo.lower().split()
    # no hago un count("grave") porque puede incluir palabras como "gravedad"
    palabras_grave = [p for p in palabras if p == "grave" or p == "graves"]
    
    return len(palabras_grave)


def get_metricas(urls):
    
    n_palabras = []
    n_tablas = []
    n_grave = []
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
    
    