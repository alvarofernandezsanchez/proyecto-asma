import mysql.connector
from dotenv import load_dotenv
import os
import pandas as pd

create_table_query = """
    CREATE DATABASE IF NOT EXISTS medicamentos_asma;

    USE medicamentos_asma;

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
    );
"""
load_dotenv()
password = os.getenv("DB_PASSWORD")

conexion = mysql.connector.connect(
    host="127.0.0.1",
    port=3306,
    user="root",
    password=password,
    connection_timeout=10
)

cursor = conexion.cursor()
print("Conexión a la base de datos establecida correctamente.")
cursor.execute(create_table_query)
print("Base de datos y tabla creadas correctamente.")


file = pd.read_csv("../../datos_completos_clusters.csv")

for index, row in file.iterrows():
    insert_query = """
        INSERT INTO medicamentos (
            nregistro, nombre, pactivos, labtitular, labcomercializador, cn, dosis,
            formaFarmaceuticaSimplificada, estado_aut, estado_rev, viasAdministracion,
            comerc, receta, generico, conduc, triangulo, huerfano, biosimilar,
            url_html_ficha_tecnica, url_foto_materiales, num_registros_atc,
            num_principios_activos, n_palabras, n_tablas, n_graves,
            estado_nomenclator, pvp_iva, precio_referencia,
            tratamiento_larga_duracion, especial_control_medico, cluster
        ) VALUES (
            %(nregistro)s, %(nombre)s, %(pactivos)s, %(labtitular)s,
            %(labcomercializador)s, %(cn)s, %(dosis)s,
            %(formaFarmaceuticaSimplificada)s, %(estado_aut)s,
            %(estado_rev)s, %(viasAdministracion)s,
            %(comerc)s, %(receta)s, %(generico)s,
            %(conduc)s, %(triangulo)s, %(huerfano)s,
            %(biosimilar)s, %(url_html_ficha_tecnica)s,
            %(url_foto_materiales)s, %(num_registros_atc)s,
            %(num_principios_activos)s, %(n_palabras)s,
            %(n_tablas)s, %(n_graves)s,
            %(estado_nomenclator)s, %(pvp_iva)s,
            %(precio_referencia)s,
            %(tratamiento_larga_duracion)s,
            %(especial_control_medico)s,
            %(cluster)s
        );
    """
    cursor.execute(insert_query, row.to_dict())
