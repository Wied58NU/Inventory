SELECT d.serial_number AS dct_serial,
       f.serial AS fin_ops_serial,
       i.service_tag AS idrac_service_tag,
       ibm.serial_nbr AS ibm_serial,
       d.vendor AS dct_make,
       d.type AS dct_type,
       d.name AS dct_name,
       f.po AS fin_ops_po,       
       i.end_date AS idrac_end_date,
       ibm.service_end_date as ibm_end_date        
FROM dct d
LEFT JOIN fin_ops_stage f on  d.serial_number = f.serial
LEFT JOIN idrac i on i.service_tag = d.serial_number
LEFT JOIN ibm ibm on ibm.serial_nbr = d.serial_number
WHERE d.type in ('SERVER','STORAGE','TAPE')
ORDER BY d.type,
         d.vendor,
         d.name;



