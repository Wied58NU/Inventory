SELECT f.tag AS fin_ops_asset_tag,
       f.po AS fin_ops_po,
       f.serial AS fin_ops_serial,
       d.serial_number AS dct_serial, 
       d.vendor AS dct_make,
       d.model AS dct_model,
       d.type AS dct_type,
       d.name AS dct_name,
       d.location
FROM fin_ops_stage f
RIGHT JOIN dct d on f.serial = d.serial_number
WHERE d.type in ('SERVER','STORAGE')
ORDER BY d.location,
         d.type,
         d.vendor,
         d.name;


