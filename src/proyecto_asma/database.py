import mysql.connector
from dotenv import load_dotenv
import os

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

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password=password,
    database="MUIAAP"
)