SELECT d.name,
       d.vendor,
       d.type,
       d.model,
       d.contact,
       d.service_owner_department,
       d.service_owner_contact,
       d.technical_contact,
       d.cabinet,
       c.function
FROM dct_stage d
LEFT JOIN cabinet_functions c ON d.cabinet = c.cabinet
WHERE c.function = 'ADMIN'
ORDER BY d.type,
         d.vendor,
         d.name,
         d.cabinet;
