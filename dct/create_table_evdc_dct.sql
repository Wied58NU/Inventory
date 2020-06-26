CREATE TABLE evdc_dct AS
SELECT d.name,
       d.vendor,
       d.type,
       d.model,
       d.serial_number,
       d.cabinet,
       c.function
FROM dct_stage d
LEFT JOIN cabinet_functions c ON d.cabinet = c.cabinet
WHERE c.function = 'ADMIN'
ORDER BY d.type,
         d.vendor,
         d.name,
         d.cabinet;


