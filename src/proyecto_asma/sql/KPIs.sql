USE medicamentos_asma;

CREATE OR REPLACE VIEW vista_kpis AS
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

    pvp_iva / num_principios_activos AS precio_por_principio,

    AVG(pvp_iva) OVER (PARTITION BY cluster) AS precio_medio_cluster,

    AVG(n_palabras) OVER (PARTITION BY cluster) AS palabras_medias_cluster,

    ROW_NUMBER() OVER (
        PARTITION BY formaFarmaceuticaSimplificada
        ORDER BY pvp_iva DESC, nregistro
    ) AS ranking_precio

FROM medicamentos;

SELECT *
FROM vista_kpis;

USE medicamentos_asma;

SELECT COUNT(*) AS total_medicamentos
FROM vista_kpis;

SHOW CREATE VIEW vista_kpis;

SELECT
    COUNT(*) AS total,
    SUM(pvp_iva IS NULL) AS sin_pvp,
    SUM(precio_referencia IS NULL) AS sin_referencia,
    SUM(densidad_ficha IS NULL) AS sin_densidad
FROM vista_kpis;