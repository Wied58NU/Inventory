SELECT d.vendor AS dct_make,
       d.model AS dct_model,
       d.type AS dct_type,
       d.name AS dct_name,
       d.serial_number,
       i.serial_nbr,
       i.service_end_date,
       i. contract_nbr
FROM dct d
LEFT JOIN ibm i on d.serial_number = i.serial_nbr
WHERE d.type in ('SERVER','STORAGE')
AND d.vendor = 'IBM'
ORDER BY d.type,
         d.vendor,
         d.name;


