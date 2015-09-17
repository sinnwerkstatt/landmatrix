--SELECT id_company FROM data.project WHERE data.project.project_code ILIKE '05%' GROUP BY id_company;

--SELECT data.project.id_company FROM data.geo_point
--JOIN data.project ON data.geo_point.project_code = data.project.project_code
--WHERE data.project.project_code ILIKE '05%' GROUP BY data.project.id_company;

SELECT data.lut_company."name_eng", data.lut_country."name_eng" FROM data.lut_company
JOIN data.lut_country ON data.lut_company.id_country = data.lut_country.id
WHERE data.lut_company.id = 2614;