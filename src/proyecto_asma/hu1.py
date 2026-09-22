import requests
import json

i = 1
datos = []

while True:
  url = f"https://cima.aemps.es/cima/rest/buscarEnFichaTecnica?pagina={i}"

  payload = json.dumps([
    {
      "seccion": "4.1",
      "texto": "asma",
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
  print(data)

nregistros = []

for pagina in datos:
  resultados = pagina["resultados"]
  for resultado in resultados:
    nregistros.append(resultado["nregistro"])

print(nregistros)