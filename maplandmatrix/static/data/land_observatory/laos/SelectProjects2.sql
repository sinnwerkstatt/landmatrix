SELECT
ST_X(ST_Transform(data.geo_point.the_geom,4326)),
ST_Y(ST_Transform(data.geo_point.the_geom,4326)),
data.project.id,
'Laos' AS "Country",
data.project.name_eng AS "Name",
data.lut_status.name_eng AS "Status",
data.project.area_ha_final AS "Size of Investment",
CASE WHEN data.doc_agreement.sign_date IS NOT NULL THEN to_char(data.doc_agreement.sign_date, 'YYYY') ELSE 0 END AS "Year of Investment (agreed)",
data.lut_sources.name_eng AS "Source",
data.lut_subsect.name_eng AS "Main Crop",
data.lut_company.id AS "Company id"
FROM data.project
JOIN data.geo_point ON data.project.project_code = data.geo_point.project_code
JOIN data.lut_status ON data.project.id_status = data.lut_status.id
JOIN data.doc_agreement ON data.project.id_doc_agreement = data.doc_agreement.id
JOIN data.lut_sources ON data.project.id_sources_status = data.lut_sources.id
JOIN data.lut_subsect ON data.project.id_subsect = data.lut_subsect.id
JOIN data.lut_company ON data.project.id_company = data.lut_company.id
WHERE data.project.project_code ILIKE '05%';