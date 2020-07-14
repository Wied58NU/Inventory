SELECT d.serial_number AS dct_serial,
       f.serial AS fin_ops_serial,
       i.service_tag AS idrac_service_tag,
       d.vendor AS dct_make,
       d.model AS dct_model,
       d.type AS dct_type,
       d.name AS dct_name,
       i.device_name AS idrac_device_name,
       f.tag AS fin_ops_asset_tag,
       f.po AS fin_ops_po,       
       i.shipped_date AS idrac_shipped_date,
       i.end_date AS idrac_end_of_support
FROM evdc_dct d
LEFT JOIN fin_ops_stage f on  d.serial_number = f.serial
RIGHT JOIN idrac i on i.service_tag = d.serial_number
WHERE d.type in ('SERVER','STORAGE')
ORDER BY d.type,
         d.vendor,
         d.name;


