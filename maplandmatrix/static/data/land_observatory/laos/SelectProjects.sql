SELECT
project.global_identifier,
p.project_code,
p.wkb_geometry,
'Lao People''s Democratic Republic' AS "Country",
lut_product.name_eng AS "Main Crop",
project.name_eng AS "name",
lut_status.name_eng AS "project_status",
area_ha_final_cde AS "size_investment",
to_char(sign_date, 'YYYY') AS "year_investment",
lut_country.name_eng AS "count_investor",
lut_company.name_eng AS "name_investor"
FROM (SELECT ST_Multi(ST_Union(the_geom)) AS wkb_geometry,project_code FROM geo_point_project GROUP BY project_code) AS p
JOIN project ON p.project_code = project.project_code
JOIN lut_product ON project.id_product = lut_product.id
JOIN lut_status ON project.id_status = lut_status.id
JOIN doc_agreement ON p.project_code = doc_agreement.project_code
JOIN lut_company ON project.id_company = lut_company.id
JOIN lut_country ON lut_company.id_country = lut_country.id
WHERE wkb_geometry && ST_GeomFromEWKT('SRID=32648;Polygon((-13850.3 1538033.14, -13850 2492781.07, 782954.34 2492781.07, 782954.34 1538033.14, -13850.3 1538033.14))')
AND area_ha_final_cde > 50

-- Create a Shapefile with ogr2ogr
-- ogr2ogr -sql "`cat lmkp/documents/external_scripts/laoimport/SelectProjects.sql`" -a_srs EPSG:32648 -lco ENCODING=UTF-8 ~/Desktop/landconcessions.shp PG:'dbname=landconcessions user=landconcessions'