SELECT i.device_name,
       i.shipped_date,
       i.end_date,
       i.service_tag,
       d.serial_number AS dct_serial, 
       d.vendor AS dct_make,
       d.model AS dct_model,
       d.type AS dct_type,
       d.name AS dct_name
FROM idrac i
RIGHT JOIN evdc_dct d on i.service_tag = d.serial_number
WHERE d.type in ('SERVER','STORAGE')
and  d.vendor = 'DELL'
and d.type = 'SERVER'
ORDER BY d.type,
         d.vendor,
         d.name;



--SELECT t1.* FROM idrac_stage t1
--JOIN 
--(
--   SELECT device_name, MAX(end_date) AS MAXDATE
--   FROM idrac_stage 
--   GROUP BY name 
--) t2
--ON T1.device_name = t2.device_name
--AND t1.date = t2.MAXDATE




