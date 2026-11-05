
import mysql.connector
from dotenv import load_dotenv
import os
import pandas as pd

# Cargar variables de entorno
load_dotenv()
password = os.getenv("DB_PASSWORD")

# Conectar con MySQL
conexion = mysql.connector.connect(
    host="127.0.0.1",
    port=3306,
    user="root",
    password=password,
    connection_timeout=10
)

cursor = conexion.cursor()

print("Conexión a la base de datos establecida correctamente.")

try:
    cursor.execute("CREATE DATABASE IF NOT EXISTS medicamentos_asma")

    cursor.execute("USE medicamentos_asma")

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS medicamentos (
            nregistro INT PRIMARY KEY,
            nombre VARCHAR(500),
            pactivos VARCHAR(500),
            labtitular VARCHAR(255),
            labcomercializador VARCHAR(255),
            cn VARCHAR(20),
            dosis VARCHAR(255),
            formaFarmaceuticaSimplificada VARCHAR(100),
            estado_aut DATETIME,
            estado_rev DATETIME NULL,
            viasAdministracion VARCHAR(255),
            comerc BOOLEAN,
            receta BOOLEAN,
            generico BOOLEAN,
            conduc BOOLEAN,
            triangulo BOOLEAN,
            huerfano BOOLEAN,
            biosimilar BOOLEAN,
            url_html_ficha_tecnica VARCHAR(500),
            url_foto_materiales VARCHAR(500),
            num_registros_atc INT,
            num_principios_activos INT,
            n_palabras INT,
            n_tablas INT,
            n_graves INT,
            estado_nomenclator VARCHAR(100),
            pvp_iva DECIMAL(10,2),
            precio_referencia DECIMAL(10,2),
            tratamiento_larga_duracion VARCHAR(10),
            especial_control_medico VARCHAR(10),
            cluster INT
        )
    """)

    print("Base de datos y tabla creadas correctamente.")

    df = pd.read_csv("datos_completos_clusters.csv")

    print("Columnas detectadas:", df.columns.tolist())

    df = df.astype(object).where(pd.notna(df), None)

    insert_query = """
        INSERT INTO medicamentos (
            nregistro, nombre, pactivos, labtitular,
            labcomercializador, cn, dosis,
            formaFarmaceuticaSimplificada, estado_aut, estado_rev,
            viasAdministracion, comerc, receta, generico,
            conduc, triangulo, huerfano, biosimilar,
            url_html_ficha_tecnica, url_foto_materiales,
            num_registros_atc, num_principios_activos,
            n_palabras, n_tablas, n_graves,
            estado_nomenclator, pvp_iva, precio_referencia,
            tratamiento_larga_duracion, especial_control_medico,
            cluster
        )
        VALUES (
            %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
            %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
            %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
        )
    """

    datos = df.values.tolist()

    cursor.executemany(insert_query, datos)

    conexion.commit()

    print(f"Se han insertado {cursor.rowcount} medicamentos.")

except Exception as e:
    conexion.rollback()
    print("Error:", e)


cursor.close()
conexion.close()
print("Conexión cerrada.")
