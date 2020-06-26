SELECT f.tag AS fin_ops_asset_tag,
       f.serial AS fin_ops_serial,
       f.po AS fin_ops_po,
       d.po_number as dct_po,
       d.serial_number AS dct_serial, 
       d.vendor AS dct_make,
       d.model AS dct_model,
       d.type AS dct_type,
       d.name AS dct_name
FROM fin_ops_stage f
RIGHT JOIN evdc_dct_po d on f.serial = d.serial_number
WHERE d.type in ('SERVER','STORAGE')
ORDER BY d.type,
         d.vendor,
         d.name;


