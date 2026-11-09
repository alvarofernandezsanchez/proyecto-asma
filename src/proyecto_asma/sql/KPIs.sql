CREATE OR REPLACE VIEW medicamentos_asma.vista_kpis AS

SELECT
    nregistro,
    nombre,
    cluster,
    formaFarmaceuticaSimplificada,
    pvp_iva,
    precio_referencia,

    (pvp_iva - precio_referencia)
        / NULLIF(precio_referencia, 0) * 100 AS desviacion_precio,

    n_palabras / NULLIF(n_tablas, 0) AS densidad_ficha,

    pvp_iva - precio_referencia AS margen_economico,

    pvp_iva / NULLIF(num_principios_activos, 0) AS precio_por_principio,

    AVG(pvp_iva) OVER (
        PARTITION BY cluster
    ) AS precio_medio_cluster,

    AVG(n_palabras) OVER (
        PARTITION BY cluster
    ) AS palabras_medias_cluster,

    CASE
        WHEN pvp_iva IS NOT NULL
        THEN ROW_NUMBER() OVER (
            PARTITION BY formaFarmaceuticaSimplificada
            ORDER BY pvp_iva DESC, nregistro
        )
    END AS ranking_precio

FROM medicamentos_asma.medicamentos;
