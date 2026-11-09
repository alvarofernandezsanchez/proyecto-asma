Use medicamentos_asma;


SELECT (n_graves / n_palabras * 100) as porcentaje_graves, n_graves, n_palabras
from medicamentos


Use medicamentos_asma;


SELECT (n_tablas / n_palabras) as ratio_tablas, n_tablas, n_palabras FROM medicamentos;


USE medicamentos_asma;
 
SELECT 
 (pvp_iva / num_principios_activos) AS precio_por_principio,
 (n_palabras / num_principios_activos) AS palabras_por_principio,
 (n_tablas / num_principios_activos) AS tablas_por_principio,
  AVG(pvp_iva) OVER (PARTITION BY cluster) AS precio_medio_cluster,
  AVG(n_palabras) OVER (PARTITION BY cluster) AS palabras_medias_cluster 
FROM medicamentos;  
 

Use medicamentos_asma;

SELECT labtitular, SUM(n_graves) AS total_terminos_graves
FROM medicamentos GROUP BY labtitular; 

USE medicamentos_asma;


SELECT nregistro, nombre, pvp_iva, precio_referencia, (pvp_iva - precio_referencia) AS margen_economico_absoluto
FROM medicamentos
WHERE pvp_iva IS NOT NULL
    AND precio_referencia IS NOT NULL
    #AND pvp_iva != precio_referencia