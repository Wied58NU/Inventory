SELECT d.name,
       d.ipaddress,
       d.type,
       d.make,
       d.model,
       d.serialnumber,
       d.cabinet,
       c.function
FROM dct d
LEFT JOIN cabinet_functions c ON d.cabinet = c.cabinet
WHERE c.function = 'ADMIN'
ORDER BY d.type,
         d.make,
         d.name,
         d.cabinet


