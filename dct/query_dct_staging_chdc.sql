SELECT d.name,
       d.type,
       d.vendor,
       d.model,
       d.service_owner_department,
       d.serial_number,
       d.cabinet
FROM dct_stage d
--LEFT JOIN cabinet_functions c ON d.cabinet = c.cabinet
WHERE d.location = 'CHDC'
ORDER BY d.type,
         d.vendor,
         d.name,
         d.cabinet


